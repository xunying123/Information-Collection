from http.client import NOT_FOUND
from typing import Annotated
from fastapi import APIRouter, Body, HTTPException
from fastapi import APIRouter
from sqlalchemy import and_, delete, exists, select
from sqlalchemy.dialects.postgresql import insert
from common.models import *
from .. import schema
from ..manager.user import current_user, login_required
from ..manager.db import db

router = APIRouter()


@router.get("/subscribe", response_model=list[schema.SiteItem])
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
def subscribe(sites_id: list[int] = Body(), keep_user_existed: bool = Body()):
    if not keep_user_existed:
        db.execute(
            delete(UserSiteRelation).where(UserSiteRelation.user_id == current_user.id)
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
def unsubscribe(site_id: int = Body()):
    db.execute(
        delete(UserSiteRelation).where(
            (UserSiteRelation.user_id == current_user.id)
            & (UserSiteRelation.site_id == site_id)
        )
    )
    return {}


@router.get("/keyword", response_model=list[schema.Keyword])
@login_required
def get_keyword(personal: bool = True):
    stmt = select(Keyword)
    if personal:
        stmt = stmt.where(
            exists().where(
                (UserKeywordRelation.user_id == current_user.id)
                & (UserKeywordRelation.keyword_id == Keyword.id)
            )
        )
    return db.scalars(stmt).all()


@router.post("/keyword")
@login_required
def add_keyword(
    words: Annotated[list[str], Body()],
    add_for_user: Annotated[bool, Body()],
    keep_user_existed: Annotated[bool, Body(embed=True)],
) -> schema.OperationMsg:
    msg = "Non change has been made"
    status = 501
    try:
        # step 1. add all keywords into database
        stmt = insert(Keyword).values(word=words).on_conflict_do_nothing()
        db.scalars(stmt).all()
        db.commit()  # allow the add of keywords seperate with user's own liked keyword
        msg = "Keywords have been added to database. But not yours."
        # step2. remove user's current keywords if needed
        if not keep_user_existed and add_for_user:
            db.execute(
                delete(UserKeywordRelation).where(
                    UserKeywordRelation.user_id == current_user.id
                )
            )
        # step3. add these keywords for user
        if add_for_user:
            user_id = current_user.id
            kw_ids = db.scalars(select(Keyword.id).where(Keyword.word.in_(words))).all()
            if len(kw_ids):
                stmt = (
                    insert(UserKeywordRelation)
                    .values([{"keyword_id": kw_id, "user_id": user_id} for kw_id in kw_ids])
                    .on_conflict_do_nothing()
                )
                db.execute(stmt)
        status = 200
        msg = "Keywords has been added successfully"
    except Exception as e:
        print(e)
    return {"status": status, "message": msg}


@router.delete("/keyword", response_model=schema.OperationMsg)
@login_required
def delete_keyword(keyword_id: int = Body(embed=True)):
    stmt = delete(UserKeywordRelation).where(
        (UserKeywordRelation.user_id == current_user.id)
        & (UserKeywordRelation.keyword_id == keyword_id)
    )
    db.execute(stmt)
    return {}
