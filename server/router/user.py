from http.client import FORBIDDEN, NOT_FOUND, UNAUTHORIZED, PRECONDITION_FAILED
from typing import Annotated
from fastapi import (
    APIRouter,
    Body,
    Depends,
    Form,
    HTTPException,
    Request,
    Response,
    Query,
)
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter
from httpx import AsyncClient
from sqlalchemy import select
from common.models import *
from server.config import JAccountAuth
from requests.auth import HTTPBasicAuth

from .. import schema
from ..manager.user import UserManager, current_user, login_manager, login_required
from ..manager.group import GroupManager
from ..manager.db import db

router = APIRouter()


@router.post("/login")
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
) -> schema.SessionToken:
    username = form.username
    password = form.password
    user = UserManager.get_user_by_username(username)
    if not UserManager.authorize(user, password):
        raise HTTPException(
            status_code=UNAUTHORIZED, detail="Incorrect username or password"
        )
    return UserManager.make_login_response(user, response)


@router.post("/logout")
@login_required
def logout(response: Response) -> schema.OperationMsg:
    response.delete_cookie(login_manager.cookie_name)
    return {"message": f"user {current_user.username} logged out"}


@router.get("/user/status")
def get_user_status() -> schema.LoginStatus:
    if current_user:
        return {"is_login": True, "user": current_user}
    else:
        return {"is_login": False}


@router.post("/register", response_model=schema.OperationMsg)
def register(data: schema.RegisterForm = Form()):
    user = UserManager.create_user(data)
    return {"message": f"User {user.name}({user.username}) created"}


@router.get("/auth")
async def do_auth_callback(request: Request, response: Response, code: str, state: str):
    try:
        print(f"{str(request.url_for("do_auth_callback"))=}")
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": str(request.url_for("do_auth_callback")),
            "client_id": JAccountAuth.client_id,
            "client_secret": JAccountAuth.secretkey,
        }
        async with AsyncClient() as client:
            res = await client.post(
                "https://jaccount.sjtu.edu.cn/oauth2/token",
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                data=data,
                auth=HTTPBasicAuth("czZCaGRSa3F0MzpnWDFmQmF0M2JW", ""),
            )
            if res.status_code != 200:
                raise HTTPException(
                    400, "Auth failed: did not get access token from jaccount"
                )
            res = res.json()
            access_token: str = res.get("access_token")
            res = await client.get(
                "https://api.sjtu.edu.cn/v1/me/profile",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if res.status_code != 200:
                raise HTTPException(
                    400, "Auth failed: did not get profile from jaccount"
                )
            profile = res.json()
        entity = profile.get("entities")[0]
        ja_code = entity.get("code")
        user = db.scalar(
            select(User).where(
                User.jaccount_code == code or User.username == entity.get("account")
            )
        )
        if user is None:
            user = User(
                jaccount_code=ja_code,
                username=entity.get("account"),
                userType=entity.get("userType"),
                name=entity.get("name"),
                organization=entity.get("organize").get("name"),
                is_admin=False,
                avatars=entity.get("accountPhotoUrl"),
            )
            db.add(user)
        else:
            user.username = entity.get("account")
            user.userType = entity.get("userType")
            user.name = entity.get("name")
            user.organization = entity.get("organize").get("name")
            user.avatars = entity.get("accountPhotoUrl")
        db.flush()
        res = RedirectResponse(state, 302)
        UserManager.make_login_response(user, res)
        return res
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"exception: {e=}")
        # return "Auth failed", 400
        raise HTTPException(400, "Auth failed")


@router.get("/group")
def get_groups() -> list[schema.Group]:
    return db.scalars(select(Group).order_by(Group.id)).all()


@login_required
def use_group_id(
    group_id: int | None = Body(None, embed=True),
) -> int | None:
    group_id = group_id if group_id else current_user.group_id
    if not group_id and not current_user.is_admin:
        raise HTTPException(
            PRECONDITION_FAILED, "No group id provided, nor user is in a group"
        )
    if (not current_user.is_admin) and (
        current_user.group_id != group_id or not current_user.group_admin
    ):
        raise HTTPException(
            UNAUTHORIZED, "You are not allowed to view this group's pending members"
        )
    return group_id


def use_group_id_strict(group_id: int | None = Depends(use_group_id)):
    if not group_id:
        raise HTTPException(
            NOT_FOUND, "does not provide group_id, or your are not in a group"
        )
    return group_id


@login_required
def use_user_id(
    user_id: int = Body(embed=True),
) -> User:
    user = UserManager.get_user_by_id(user_id)
    if not user:
        raise HTTPException(NOT_FOUND, "user does not exist.")
    return user


@router.get("/group/members/pending")
@login_required
def get_pending_members(
    group_id: int | None = Depends(use_group_id_strict),
) -> list[schema.User]:
    stmt = (
        select(User)
        .where(User.group_accepted == False)
        .where(User.group_id == group_id)
    )
    return db.scalars(stmt).all()


@router.get("/group/members")
@login_required
def get_group_users(
    group_id: int | None = Query(None, description="only effects when user is admin.")
) -> list[schema.User]:
    if current_user.is_admin and group_id:
        group = GroupManager.get_group_from_id(group_id)
        return group.users
    if not current_user.group_id or (
        not current_user.group_admin and not current_user.is_admin
    ):
        raise HTTPException(NOT_FOUND, "You are not an admin of some group")
    # print(f"{current_user.group}")
    # print(f"{current_user.group.users}")
    return current_user.group.users


@router.post("/group/members")
@login_required
def add_user_to_group(
    user: User = Depends(use_user_id), group_id: int = Depends(use_group_id_strict)
) -> schema.OperationMsg:
    if user.group_id and user.group_id != group_id:
        return schema.OperationMsg(status=-1, message="user has been in another group")
    user.group_id = group_id
    user.group_accepted = True
    return {}


@router.delete("/group/members")
@login_required
def remove_user_from_group(user: User = Depends(use_user_id)) -> schema.OperationMsg:
    if current_user.is_admin:
        UserManager.leave_group(user)
        return {}
    if not current_user.group_admin:
        raise HTTPException(
            FORBIDDEN, "you do not have the permission to manage this group."
        )
    if current_user.group_id != user.group_id:
        return schema.OperationMsg(
            status=-1, message="the user does not in your group."
        )
    UserManager.leave_group(user)
    return {}


@router.post("/group/leave")
@login_required
def leave_group() -> schema.OperationMsg:
    current_user.group_id = None
    current_user.group_accepted = False
    current_user.group_admin = False
    return {}


@router.get("/user/free")
@login_required
def get_userinfo_not_in_group(username: str) -> schema.User | None:
    if not (current_user.is_admin or current_user.group_admin):
        raise HTTPException(FORBIDDEN, "your are not an admin.")
    user = UserManager.get_user_by_username(username)
    if user and user.group_id:
        user = None
    return user
