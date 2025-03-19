from http.client import NOT_FOUND, UNAUTHORIZED
from typing import Annotated
from fastapi import APIRouter, Body, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter
from httpx import AsyncClient
from sqlalchemy import and_, delete, exists, select
from sqlalchemy.dialects.postgresql import insert
from common.models import *
from server.config import JAccountAuth
from requests.auth import HTTPBasicAuth
from .. import schema
from ..manager.user import UserManager, current_user, login_manager, login_required
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
def register(data: schema.RegisterForm):
    return {"status": 501, "message": f"Not Implemented, {str(data)}"}


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


# @router.post("/group", response_model=schema.OperationMsg)
# def add_group(user_id: int, group: str):
#     pass


# @router.delete("/group", response_model=schema.OperationMsg)
# def delete_group(user_id: int):
#     pass
