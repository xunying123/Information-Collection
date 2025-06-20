from http.client import (
    FORBIDDEN,
    FOUND,
    INTERNAL_SERVER_ERROR,
    NOT_FOUND,
    TEMPORARY_REDIRECT,
    UNAUTHORIZED,
    PRECONDITION_FAILED,
)
from typing import Annotated, Any
from urllib.parse import urlencode
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
from httpx import AsyncClient, BasicAuth
from sqlalchemy import select
from common.models import *
from server import config
from server.config import OAUTH_MAP, AuthCNAES, JAccountAuth

from server.manager.oauth import cnaes_from_token, jaccount_from_token

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
    if not user or not UserManager.authorize(user, password):
        raise HTTPException(
            status_code=UNAUTHORIZED, detail="Incorrect username or password"
        )
    return UserManager.make_login_response(user, response)


@router.post("/logout")
@login_required
def logout(response: Response) -> schema.OperationMsg:
    response.delete_cookie(login_manager.cookie_name)
    return schema.OperationMsg(message=f"user {current_user.username} logged out")


@router.get("/user/status", response_model=schema.LoginStatus)
def get_user_status():
    if current_user:
        return {"is_login": True, "user": current_user}
    else:
        return {"is_login": False}


@router.post("/register", response_model=schema.OperationMsg)
def register(data: schema.RegisterForm = Form()):
    user = UserManager.create_user(data)
    return schema.OperationMsg(message=f"User {user.name}({user.username}) created")


def oauth_callback_url(request: Request, provider: str) -> str:
    return str(request.url_for("do_auth_callback", provider=provider)).replace(
        ":80/", "/"
    )


@router.get("/login/oauth/{provider}")
async def redirect2oauth(
    provider: str, state: str, cb_url: str = Depends(oauth_callback_url)
):
    auth_config = OAUTH_MAP[provider]
    if not auth_config:
        raise HTTPException(400, "Auth failed: unknown provider")
    query = urlencode(
        {
            "client_id": auth_config.client_id,
            "response_type": "code",
            "redirect_uri": cb_url,
            "state": state,
        }
    )
    redirect_uri = f"{auth_config.auth_url}?{query}"
    return RedirectResponse(redirect_uri, TEMPORARY_REDIRECT)


async def get_access_token(
    code: str, redirect_uri: str, auth_config: config.OauthConfig
) -> Any:
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": auth_config.client_id,
        "client_secret": auth_config.secret_key,
    }
    async with AsyncClient() as client:
        res = await client.post(
            auth_config.token_url,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data,
            auth=BasicAuth("czZCaGRSa3F0MzpnWDFmQmF0M2JW", ""),
        )
        print(res.json())
        if res.status_code != 200:
            raise HTTPException(
                400, "Auth failed: did not get access token from jaccount"
            )
        res = res.json()
    return res


@router.get("/auth/{provider}")
async def do_auth_callback(
    request: Request,
    provider: str,
    code: str,
    state: str,
    cb_url: str = Depends(oauth_callback_url),
):
    auth_config = OAUTH_MAP[provider]
    if not auth_config:
        raise HTTPException(400, "Auth failed: unknown provider")
    try:
        res = await get_access_token(code, cb_url, auth_config)
        match provider:
            case JAccountAuth.name:
                user = await jaccount_from_token(res)
            case AuthCNAES.name:
                user = cnaes_from_token(res)
            case _:
                raise HTTPException(400, "Auth failed: unknown provider")
        res = RedirectResponse(state, FOUND)
        UserManager.make_login_response(user, res)
        return res
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(INTERNAL_SERVER_ERROR, "Auth failed")


@router.get("/group", response_model=list[schema.Group])
def get_groups():
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


@router.get("/group/members/pending", response_model=list[schema.User])
@login_required
def get_pending_members(
    group_id: int | None = Depends(use_group_id_strict),
):
    stmt = (
        select(User)
        .where(User.group_accepted == False)
        .where(User.group_id == group_id)
    )
    return db.scalars(stmt).all()


@router.get("/group/members", response_model=list[schema.User])
@login_required
def get_group_users(
    group_id: int | None = Query(None, description="only effects when user is admin.")
):
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
    return schema.OperationMsg()


@router.delete("/group/members")
@login_required
def remove_user_from_group(user: User = Depends(use_user_id)) -> schema.OperationMsg:
    if current_user.is_admin:
        UserManager.leave_group(user)
        return schema.OperationMsg()
    if not current_user.group_admin:
        raise HTTPException(
            FORBIDDEN, "you do not have the permission to manage this group."
        )
    if current_user.group_id != user.group_id:
        return schema.OperationMsg(
            status=-1, message="the user does not in your group."
        )
    UserManager.leave_group(user)
    return schema.OperationMsg()


@router.post("/group/leave")
@login_required
def leave_group() -> schema.OperationMsg:
    current_user.group_id = None
    current_user.group_accepted = False
    current_user.group_admin = False
    return schema.OperationMsg()


@router.get("/user/free", response_model=schema.User | None)
@login_required
def get_userinfo_not_in_group(username: str):
    if not (current_user.is_admin or current_user.group_admin):
        raise HTTPException(FORBIDDEN, "your are not an admin.")
    user = UserManager.get_user_by_username(username)
    if user and user.group_id:
        user = None
    return user
