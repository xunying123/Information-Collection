from fastapi import APIRouter
from sqlalchemy import exists, or_, select, func
import pytz
from ..schema import *
from ..manager.login import current_user
from ..manager.db import db

router = APIRouter()

@router.get("/page", response_model=list[ResPageItem])
def get_pages(
    today: bool = False,
    keyword: bool = False,
    subscribe: bool = False,
    bookmarked: bool = False,
    cursor_id: int = 0,
    count: int = 0,
    time_start: datetime | None = None,
    time_end: datetime | None = None,
    search_title: str = "",
    search_content: str = "",
    site: int | None = None,
    category: int | list[int] | None = None,
):
    stmt = select(Page).order_by(Page.created_at.desc())
    if today:
        shanghai_tz = pytz.timezone("Asia/Shanghai")
        today = datetime.now(shanghai_tz).date()
        stmt = stmt.where(func.date(Page.publish_time) == today)
    if bookmarked:
        stmt = stmt.join(Bookmark).where(Bookmark.user_id == current_user.id)
    if keyword:
        stmt = stmt.where(
            exists().where(
                (UserKeywordRelation.user_id == current_user.id)
                & (UserKeywordRelation.keyword_id == Keyword.id)
                & (Keyword.id == PageKeywordRelation.keyword_id)
                & (PageKeywordRelation.page_id == Page.id)
            )
        )
    if subscribe:
        stmt = stmt.where(
            exists().where(
                (UserSiteRelation.user_id == current_user.id)
                & (UserSiteRelation.site_id == Site.id)
                & (Site.id == Page.site_id)
            )
        )
    if cursor_id > 0:
        stmt = stmt.where(Page.id < cursor_id)
    if count > 0:
        stmt = stmt.limit(count)
    if time_start:
        stmt = stmt.where(Page.publish_time >= time_start)
    if time_end:
        stmt = stmt.where(Page.publish_time <= time_end)
    if search_title and search_content:
        stmt = stmt.where(
            or_(
                Page.title.like(f"%{search_title}%"),
                Page.full_content.like(f"%{search_content}%"),
            )
        )
    elif search_title:
        stmt = stmt.where(Page.title.like(f"%{search_title}%"))
    elif search_content:
        stmt = stmt.where(Page.full_content.like(f"%{search_content}%"))
    sites_id = None
    if site is not None:
        sites_id = [site]
    elif category is not None:
        # special logic: count is used to limit every SITE instead of total pages
        # cursor_id should not be used in this case CURRENTLY
        # TODO: support cursor_id in this case
        if type(category) is int:
            sites_id = db.scalars(select(Site.id).where(Site.cate_id == category))
        elif type(category) is list:
            sites_id = db.scalars(select(Site.id).where(Site.cate_id.in_(category)))
        else:
            raise ValueError("invalid category type")

    result = []

    def get_once(stmt):
        result.extend(db.scalars(stmt).all())

    if sites_id is not None:
        for site_id in sites_id:
            get_once(stmt.where(Page.site_id == site_id))
    else:
        get_once(stmt)
    new_cursor_id = min([x["id"] for x in result]) if result else None
    # todo: 返回类型需要修改
    return {"pages": result, "cursor_id": new_cursor_id}


@router.get("/category", response_model=list[ResCategory])
def get_category():
    stmt = select(Category).order_by(Category.id)
    res = db.scalars(stmt).all()
    return res


@router.get("/category/{cate_id}", response_model=ResCategory)
def get_category(cate_id: int):
    stmt = select(Category).where(Category.id == cate_id)
    res = db.scalar(stmt)
    return res


@router.post("/category", response_model=ResOperationMsg)
def add_category(name: str):
    if db.scalar(select(Category.id).where(Category.name == name)) is not None:
        return {"status": 400, "message": "category already exists"}
    cate = Category(name=name)
    db.add(cate)
    db.flush()
    return {"status": 200, "message": "success"}


@router.get("/site", response_model=list[ResSiteItem])
def get_site(subscribe: bool = False, category: int | None = None):
    result = []
    stmt = select(Site).order_by(Site.cate_id, Site.id).where(Site.disabled == False)
    if category is not None:
        stmt = stmt.where(Site.cate_id == category)
    if subscribe:
        stmt = stmt.where(
            exists().where(
                (UserSiteRelation.user_id == current_user.id)
                & (UserSiteRelation.site_id == Site.id)
            )
        )
    return db.scalars(stmt).all()


@router.get("/site/{site_id}", response_model=ResSite)
def get_site(site_id: int):
    stmt = select(Site).filter(Site.id == site_id)
    res = db.scalar(stmt)
    return res


@router.post("/site", response_model=ResOperationMsg)
def add_site(name: str, url: str, cate_id: int, icon: str):
    site = Site(name=name, url=url, cate_id=cate_id, icon=icon)
    db.add(site)
    db.flush()
    site_id = site.id
    # return type 需要修改
    return {"status": 200, "message": "success", "site_id": site_id}


@router.delete("/site{site_id}", response_model=ResOperationMsg)
def delete_site(site_id: int):
    site = db.scalar(select(Site).where(Site.id == site_id))
    if site is None:
        return {"status": 400, "message": f"site {site_id} not found"}
    site.disabled = True
    return {"status": 200, "message": "success"}


@router.get("/page/{page_id}")
def get_page(page_id: int):
    stmt = select(Page).where(Page.id == page_id)
    page = db.scalar(stmt)
    if page is None:
        return {"status": 400, "message": f"page {page_id} not found"}
    # todo: 返回类型需要修改
    return page


