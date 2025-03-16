from typing import Annotated
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter
from sqlalchemy import and_, delete, exists, select
from ..schema import *
from ..manager.login import current_user, login_manager
from ..manager.db import db

router = APIRouter()


@router.post("/login")
async def login(
    form: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response
):
    # username = form.username
    # password = form.password
    token = login_manager.create_access_token(data={"sub": f"1"})
    response.set_cookie(
        key=login_manager.cookie_name, value=token, httponly=True, samesite="lax"
    )
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout", response_model=ResOperationMsg)
def logout():
    pass

@router.get("/subscribe", response_model=list[ResSiteItem])
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


@router.post("/subscribe", response_model=ResOperationMsg)
def subscribe(sites_id: list[int], keep_user_existed: bool):
    if not keep_user_existed:
        db.execute(
            UserSiteRelation.delete().where(UserSiteRelation.user_id == current_user.id)
        )
    for site_id in sites_id:
        site = db.scalar(select(Site).where(Site.id == site_id))
        if site is None:
            return {"status": 400, "message": f"site {site_id} not found"}
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
    return {"status": 200, "message": "success"}


@router.delete("/subscribe", response_model=ResOperationMsg)
def unsubscribe(site_id: int):
    db.execute(
        delete(UserSiteRelation).where(
            (UserSiteRelation.user_id == current_user.id)
            & (UserSiteRelation.site_id == site_id)
        )
    )
    return {"status": 200, "message": "success"}


@router.get("/keyword")
def get_keyword(personal: bool):
    stmt = select(Keyword)
    if personal:
        stmt = stmt.where(
            exists().where(
                (UserKeywordRelation.user_id == current_user.id)
                & (UserKeywordRelation.keyword_id == Keyword.id)
            )
        )
    result = []
    for kw in db.scalars(stmt):
        info = ResponseKeywordItem(kw)
        result.append(info)


@router.post("/keyword", response_model=ResOperationMsg)
def add_keyword(words: list[str], add_for_user: bool, keep_user_existed: bool):
    kw_ids = []
    if not keep_user_existed and add_for_user:
        db.execute(
            delete(UserKeywordRelation).where(
                UserKeywordRelation.user_id == current_user.id
            )
        )
    for word in words:
        kw = db.scalar(select(Keyword).where(Keyword.word == word))
        if kw is None:
            kw = Keyword(word=word)
            db.add(kw)
            db.flush()
            kw_id = kw.id
        else:
            kw_id = kw.id
        if add_for_user:
            if (
                db.scalar(
                    select(UserKeywordRelation).where(
                        (UserKeywordRelation.user_id == current_user.id)
                        & (UserKeywordRelation.keyword_id == kw_id)
                    )
                )
                is not None
            ):
                continue
            db.add(UserKeywordRelation(user_id=current_user.id, keyword_id=kw_id))
        kw_ids.append(kw_id)
    return {"status": 200, "message": "success"}


@router.delete("/keyword", response_model=ResOperationMsg)
def delete_keyword(keyword_id: int):
    stmt = delete(UserKeywordRelation).where(
        (UserKeywordRelation.user_id == current_user.id)
        & (UserKeywordRelation.keyword_id == keyword_id)
    )
    db.execute(stmt)


@router.post("/group", response_model=ResOperationMsg)
def add_group(user_id: int, group: str):
    pass


@router.delete("/group", response_model=ResOperationMsg)
def delete_group(user_id: int):
    pass


@router.get("/user/me")
def get_user():
    pass
    # ...
    # （审核中）


@router.post("/register", response_model=ResOperationMsg)
def register(user_name: str, password: str, group: str):
    pass


