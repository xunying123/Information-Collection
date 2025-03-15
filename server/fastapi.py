from fastapi import Depends, FastAPI
import pytz
from sqlalchemy import exists, or_, select
from common.models import *
from server.request_format import *
from .response_format import *
from .db import db
from .login import current_user

app = FastAPI(root_path="/api", dependencies=[Depends(db.app_dependency)])


@app.get("/page", response_model=list[ResPageItem])
def search_page(data: PageGet):
    only_today = data.today
    filterd_by_keyword = data.keyword
    filterd_by_subscribe = data.subscribe

    stmt = select(Page).order_by(Page.created_at.desc())
    if only_today:
        shanghai_tz = pytz.timezone("Asia/Shanghai")
        today = datetime.now(shanghai_tz).date()
        stmt = stmt.where(func.date(Page.publish_time) == today)
    if data.bookmarked:
        stmt = stmt.join(Bookmark).where(Bookmark.user_id == current_user.id)
    if filterd_by_keyword:
        stmt = stmt.where(
            exists().where(
                (UserKeywordRelation.user_id == current_user.id)
                & (UserKeywordRelation.keyword_id == Keyword.id)
                & (Keyword.id == PageKeywordRelation.keyword_id)
                & (PageKeywordRelation.page_id == Page.id)
            )
        )
    if filterd_by_subscribe:
        stmt = stmt.where(
            exists().where(
                (UserSiteRelation.user_id == current_user.id)
                & (UserSiteRelation.site_id == Site.id)
                & (Site.id == Page.site_id)
            )
        )
    # cursor_id should be avoid when category is set but site is not
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
            sites_id = db.scalars(select(Site.id).where(Site.cate_id == data.category))
        elif type(data.category) is list:
            sites_id = db.scalars(
                select(Site.id).where(Site.cate_id.in_(data.category))
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
    new_cursor_id = min([x["id"] for x in result]) if result else None
    return {"pages": result, "cursor_id": new_cursor_id}


@app.get("/category", response_model=list[ResCategory])
def get_category():
    stmt = select(Category).order_by(Category.id)
    res = db.scalars(stmt).all()
    return res


@app.get("/catagory/{cate_id}", response_model=ResCategory)
def get_category(cate_id: int):
    pass


@app.post("/category")
def add_category():
    pass


@app.get("/site", response_model=list[ResSiteItem])
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


@app.get("/site/{site_id}", response_model=ResSite)
def get_site(site_id: int):
    stmt = select(Site).filter(Site.id == site_id)
    res = db.scalar(stmt)
    return res


@app.post("/site", response_model=ResOperationMsg)
def add_site(name: str, url: str, category: int, icon: str): ...


@app.delete("/site{site_id}", response_model=ResOperationMsg)
def delete_site(site_id: int): ...


@app.get("/page/{page_id}")
def get_page(page_id: int):
    pass


@app.get("/page", response_model=list[ResPageItem])
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
    pass


@app.get("/subscribe", response_model=list[ResSiteItem])
def get_subscribe():
    pass


@app.post("/subscribe", response_model=ResOperationMsg)
def subscribe(sites_id: list[int], keep_user_existed: bool):
    pass


@app.delete("/subscribe", response_model=ResOperationMsg)
def unsubscribe(site_id: int):
    pass


@app.get("/keyword")
def get_keyword(personal: bool):
    pass


@app.post("/keyword", response_model=ResOperationMsg)
def add_keyword(wors: list[str], add_for_user: bool, keep_user_existed: bool):
    pass


@app.delete("/keyword", response_model=ResOperationMsg)
def delete_keyword(word_id: int):
    pass


@app.get("/user/me")
def get_user():
    pass


@app.post("/register", response_model=ResOperationMsg)
def register(username: str, password: str, organization: str):
    pass


@app.post("/login", response_model=ResOperationMsg)
def login(username: str, password: str):
    pass
    # 用户不存在
    # 密码错误
    # 登录成功


@app.post("/logout", response_model=ResOperationMsg)
def logout():
    pass
