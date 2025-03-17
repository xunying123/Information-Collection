from http.client import NOT_FOUND, UNAUTHORIZED
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter
from httpx import AsyncClient
from sqlalchemy import and_, delete, exists, insert, select
from common.models import *
from server.config import JAccountAuth
from requests.auth import HTTPBasicAuth
from .. import schema

# from ..schema import *
from ..manager.user import UserManager, current_user, login_manager, login_required
from ..manager.db import db

router = APIRouter()


@router.post("/login")
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
):
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
def register(user_name: str, password: str):
    raise NotImplementedError


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


@router.get("/subscribe", response_model=list[schema.ResSiteItem])
@login_required
def get_subscribe():
    stmt = select(Site).where(
        and_(
            exists().where(
                (UserSiteRelation.user_id == current_user.id)
                & (UserSiteRelation.site_id == Site.id)
            ),
            Site.disabled == False,
        )
    )
    return db.scalars(stmt).all()


@router.post("/subscribe", response_model=schema.OperationMsg)
@login_required
def subscribe(sites_id: list[int], keep_user_existed: bool):
    if not keep_user_existed:
        db.execute(
            UserSiteRelation.delete().where(UserSiteRelation.user_id == current_user.id)
        )
    for site_id in sites_id:
        site = db.scalar(select(Site).where(Site.id == site_id))
        if site is None:
            raise HTTPException(NOT_FOUND, f"site {site_id} not found")
        if (
            db.scalar(
                select(UserSiteRelation)
                .where(UserSiteRelation.user_id == current_user.id)
                .where(UserSiteRelation.site_id == site_id)
            )
            is not None
        ):
            continue
        db.add(UserSiteRelation(user_id=current_user.id, site_id=site_id))
    return {}


@router.delete("/subscribe", response_model=schema.OperationMsg)
@login_required
def unsubscribe(site_id: int):
    db.execute(
        delete(UserSiteRelation).where(
            (UserSiteRelation.user_id == current_user.id)
            & (UserSiteRelation.site_id == site_id)
        )
    )
    return {}


@router.get("/keyword", response_model=list[schema.Keyword])
@login_required
def get_keyword(personal: bool):
    stmt = select(Keyword)
    if personal:
        stmt = stmt.where(
            exists().where(
                (UserKeywordRelation.user_id == current_user.id)
                & (UserKeywordRelation.keyword_id == Keyword.id)
            )
        )
    return db.scalars(stmt).all()


@router.post("/keyword", response_model=schema.OperationMsg)
@login_required
def add_keyword(words: list[str], add_for_user: bool, keep_user_existed: bool):
    if not keep_user_existed and add_for_user:
        db.execute(
            delete(UserKeywordRelation).where(
                UserKeywordRelation.user_id == current_user.id
            )
        )
    keywords = [Keyword(word=word) for word in words]
    stmt = (
        insert(Keyword).values(keywords).on_conflict_do_nothing().returning(Keyword.id)
    )
    kw_ids = db.scalars(stmt).all()
    if add_for_user:
        user_kw_relations = [
            UserKeywordRelation(user_id=current_user.id, keyword_id=kw_id)
            for kw_id in kw_ids
        ]
        stmt = (
            insert(UserKeywordRelation)
            .values(user_kw_relations)
            .on_conflict_do_nothing()
        )
        db.execute(stmt)
    return {}


@router.delete("/keyword", response_model=schema.OperationMsg)
@login_required
def delete_keyword(keyword_id: int):
    stmt = delete(UserKeywordRelation).where(
        (UserKeywordRelation.user_id == current_user.id)
        & (UserKeywordRelation.keyword_id == keyword_id)
    )
    db.execute(stmt)
    return {}


# @router.post("/group", response_model=schema.OperationMsg)
# def add_group(user_id: int, group: str):
#     pass


# @router.delete("/group", response_model=schema.OperationMsg)
# def delete_group(user_id: int):
#     pass
