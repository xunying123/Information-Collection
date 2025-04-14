import pytz
from http.client import NOT_FOUND
from fastapi import APIRouter, HTTPException
from sqlalchemy import exists, or_, select, func
from common.models import *
from server import schema
from ..manager.user import current_user, login_required
from ..manager.db import db

router = APIRouter()


@router.post("/pages", response_model=schema.PagedQuery[schema.PageItem])
@login_required
def get_pages(data: schema.PageGet):
    stmt = select(Page).order_by(Page.created_at.desc())
    if data.today:
        shanghai_tz = pytz.timezone("Asia/Shanghai")
        today = datetime.now(shanghai_tz).date()
        stmt = stmt.where(func.date(Page.publish_time) == today)
    if data.bookmarked:
        stmt = stmt.join(Bookmark).where(Bookmark.user_id == current_user.id)
    if data.filter_user_keyword:
        stmt = stmt.where(
            exists().where(
                (UserKeywordRelation.user_id == current_user.id)
                & (UserKeywordRelation.keyword_id == Keyword.id)
                & (Keyword.id == PageKeywordRelation.keyword_id)
                & (PageKeywordRelation.page_id == Page.id)
            )
        )
    if data.subscribe > 0:
        stmt = stmt.where(
            exists().where(
                (UserSiteRelation.user_id == current_user.id)
                & (UserSiteRelation.site_id == Site.id)
                & (UserSiteRelation.negative == False)
                & (Site.id == Page.site_id)
            )
        )
    elif data.subscribe < 0:
        stmt = stmt.where(
            ~exists().where(
                (UserSiteRelation.user_id == current_user.id)
                & (UserSiteRelation.site_id == Site.id)
                & (UserSiteRelation.negative == True)
                & (Site.id == Page.site_id)
            )
        )
    if data.cursor_id > 0:
        stmt = stmt.where(Page.id < data.cursor_id)
    if data.count > 0:
        stmt = stmt.limit(data.count)
    if data.time_start:
        stmt = stmt.where(Page.publish_time >= data.time_start)
    if data.time_end:
        stmt = stmt.where(Page.publish_time <= data.time_end)
    if data.search_title and data.search_content:
        stmt = stmt.where(
            or_(
                Page.title.like(f"%{data.search_title}%"),
                Page.full_content.like(f"%{data.search_content}%"),
            )
        )
    elif data.search_title:
        stmt = stmt.where(Page.title.like(f"%{data.search_title}%"))
    elif data.search_content:
        stmt = stmt.where(Page.full_content.like(f"%{data.search_content}%"))
    sites_id = None
    if data.site is not None:
        sites_id = [data.site]
    elif data.category is not None:
        # special logic: count is used to limit every SITE instead of total pages
        # cursor_id should not be used in this case CURRENTLY
        # TODO: support cursor_id in this case
        if type(data.category) is int:
            data.category = [data.category]
        if type(data.category) is list:
            sites_id = db.scalars(
                select(Site.id)
                .join(CategorySiteRelation)
                .where(CategorySiteRelation.category_id.in_(data.category))
            )
        else:
            raise ValueError("invalid category type")

    if type(data.subject) is int:
        data.subject = [data.subject]
    if type(data.subject) is list:
        stmt = stmt.join(
            SubjectKeywordRelation, SubjectKeywordRelation.subject_id.in_(data.subject)
        ).join(
            PageKeywordRelation,
            (PageKeywordRelation.keyword_id == SubjectKeywordRelation.keyword_id)
            & (PageKeywordRelation.page_id == Page.id),
        )

    result: list[Page] = []

    def get_once(stmt):
        result.extend(db.scalars(stmt).all())

    if sites_id is not None:
        for site_id in sites_id:
            get_once(stmt.where(Page.site_id == site_id))
    else:
        get_once(stmt)
    new_cursor_id = min([x.id for x in result]) if result else None
    return {"data": result, "cursor_id": new_cursor_id}


@router.get("/site", response_model=list[schema.SiteItem])
@login_required
def get_sites():
    stmt = select(Site).order_by(Site.id).where(Site.disabled == False)
    return db.scalars(stmt).all()


@router.get("/site/{site_id}", response_model=schema.Site)
@login_required
def get_site(site_id: int):
    stmt = select(Site).where(Site.id == site_id)
    site = db.scalar(stmt)
    if site is None:
        raise HTTPException(NOT_FOUND, f"site {site_id} not found")
    return site


@router.post("/site", response_model=schema.OperationMsg)
@login_required
def add_site(data: schema.SiteItem):
    site = Site(name=data.name, url=data.url, icon=data.icon)
    db.add(site)
    db.flush()
    site_id = site.id
    return {"status": 200, "message": "success", "site_id": site_id}


# @router.delete("/site{site_id}", response_model=schema.OperationMsg)
# @login_required
# def delete_site(site_id: int):
#     site = db.scalar(select(Site).where(Site.id == site_id))
#     if site is None:
#         return {"status": 400, "message": f"site {site_id} not found"}
#     site.disabled = True
#     return {"status": 200, "message": "success"}


@router.get("/page/{page_id}", response_model=schema.Page)
@login_required
def get_page(page_id: int):
    stmt = select(Page).where(Page.id == page_id)
    page = db.scalar(stmt)
    if page is None:
        raise HTTPException(NOT_FOUND, f"page {page_id} not found")
    return page
