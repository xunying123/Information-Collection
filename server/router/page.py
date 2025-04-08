import pytz
from http.client import NOT_FOUND, PRECONDITION_FAILED
from fastapi import APIRouter, HTTPException, Body
from sqlalchemy import exists, or_, select, func, delete
from common.models import *
from server import schema
from ..manager.user import current_user, login_required
from ..manager.db import db
from ..manager.group import current_group, group_admin_required, group_required

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
    if data.keyword:
        stmt = stmt.where(
            exists().where(
                (UserKeywordRelation.user_id == current_user.id)
                & (UserKeywordRelation.keyword_id == Keyword.id)
                & (Keyword.id == PageKeywordRelation.keyword_id)
                & (PageKeywordRelation.page_id == Page.id)
            )
        )
    if data.subscribe:
        stmt = stmt.where(
            exists().where(
                (UserSiteRelation.user_id == current_user.id)
                & (UserSiteRelation.site_id == Site.id)
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


@router.get("/category", response_model=list[schema.Category])
@group_required
def get_categories():
    return current_group.categories


@router.get("/category/{cate_id}", response_model=schema.Category)
@login_required
def get_category(cate_id: int):
    stmt = select(Category).where(Category.id == cate_id)
    res = db.scalar(stmt)
    return res


@router.post("/category", response_model=schema.OperationMsg)
@group_admin_required
def add_category(category: schema.CategoryItem):
    if (
        db.scalar(
            select(Category.id).where(
                Category.name == category.name
                and Category.belonged_group_id == current_group.id
            )
        )
        is not None
    ):
        raise HTTPException(PRECONDITION_FAILED, "category already exists")
    cate = Category(name=category.name, belonged_group_id=current_group.id)
    db.add(cate)
    return {}


@router.post("/category/site", response_model=schema.OperationMsg)
@group_admin_required
def add_site_to_category(cate_id: int = Body(), site_id: int = Body()):
    if (
        db.scalar(select(Category.belonged_group_id).where(Category.id == cate_id))
        != current_group.id
    ):
        raise HTTPException(PRECONDITION_FAILED, "category not in current group")
    if db.scalar(
        select(CategorySiteRelation)
        .where(CategorySiteRelation.category_id == cate_id)
        .where(CategorySiteRelation.site_id == site_id)
    )  is not None:
        return schema.OperationMsg(message="site already added into this category")
    rel = CategorySiteRelation(site_id=site_id, category_id=cate_id)
    db.add(rel)
    return {}


@router.delete("/category/site", response_model=schema.OperationMsg)
@group_admin_required
def remove_site_from_category(cate_id: int = Body(), site_id: int = Body()):
    if (
        db.scalar(select(Category.belonged_group_id).where(Category.id == cate_id))
        != current_group.id
    ):
        raise HTTPException(PRECONDITION_FAILED, "category not in current group")
    stmt = delete(CategorySiteRelation).where(CategorySiteRelation.category_id == cate_id).where(CategorySiteRelation.site_id == site_id)
    db.execute(stmt)
    return {}


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
