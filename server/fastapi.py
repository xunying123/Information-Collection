from fastapi import Depends, FastAPI
import pytz
from sqlalchemy import exists, or_, select, and_, delete
from common.models import *
from server.request_format import *
from .response_format import *
from .db import db
from .login import current_user

app = FastAPI(root_path="/api", dependencies=[Depends(db.app_dependency), Depends(current_user.app_dependency)])


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


@app.get("/category/{cate_id}", response_model=ResCategory)
def get_category(cate_id: int):
    stmt = select(Category).where(Category.id == cate_id)
    res = db.scalar(stmt)
    return res


@app.post("/category", response_model=ResOperationMsg)
def add_category(name: str):
    if db.scalar(select(Category.id).where(Category.name == name)) is not None:
        return {"status": 400, "message": "category already exists"}
    cate = Category(name=name)
    db.add(cate)
    db.flush()
    return {"status": 200, "message": "success"}


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
def add_site(name: str, url: str, cate_id: int, icon: str):
    site = Site(name=name, url=url, cate_id=cate_id, icon=icon)
    db.add(site)
    db.flush()
    site_id = site.id
    # return type 需要修改
    return {"status": 200, "message": "success", "site_id": site_id}


@app.delete("/site{site_id}", response_model=ResOperationMsg)
def delete_site(site_id: int):
    site = db.scalar(select(Site).where(Site.id == site_id))
    if site is None:
        return {"status": 400, "message": f"site {site_id} not found"}
    site.disabled = True
    return {"status": 200, "message": "success"}


@app.get("/page/{page_id}")
def get_page(page_id: int):
    stmt = select(Page).where(Page.id == page_id)
    page = db.scalar(stmt)
    if page is None:
        return {"status": 400, "message": f"page {page_id} not found"}
    # todo: 返回类型需要修改    
    return page


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
            sites_id = db.scalars(
                select(Site.id).where(Site.cate_id.in_(category))
            )
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


@app.get("/subscribe", response_model=list[ResSiteItem])
def get_subscribe():
    stmt = select(Site).where(
        and_(
            exists().where(
                (UserSiteRelation.user_id == current_user.id)
                & (UserSiteRelation.site_id == Site.id)
            ),
            Site.disabled == False
        )
    )
    return db.scalars(stmt).all()


@app.post("/subscribe", response_model=ResOperationMsg)
def subscribe(sites_id: list[int], keep_user_existed: bool):
    if not keep_user_existed:
        db.execute(UserSiteRelation.delete().where(UserSiteRelation.user_id == current_user.id))
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

@app.delete("/subscribe", response_model=ResOperationMsg)
def unsubscribe(site_id: int):
    db.execute(
        delete(UserSiteRelation).where(
            (UserSiteRelation.user_id == current_user.id)
            & (UserSiteRelation.site_id == site_id)
        )
    )
    return {"status": 200, "message": "success"}


@app.get("/keyword")
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

@app.post("/keyword", response_model=ResOperationMsg)
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


@app.delete("/keyword", response_model=ResOperationMsg)
def delete_keyword(keyword_id: int):
    stmt = delete(UserKeywordRelation).where(
        (UserKeywordRelation.user_id == current_user.id)
        & (UserKeywordRelation.keyword_id == keyword_id)
    )
    db.execute(stmt)

@app.post("/group", response_model=ResOperationMsg)
def add_group(user_id: int, group: str):
    pass

@app.delete("/group", response_model=ResOperationMsg)
def delete_group(user_id: int):
    pass

@app.get("/user/me")
def get_user():
    pass
    # ...
    # （审核中）

@app.post("/register", response_model=ResOperationMsg)
def register(user_name: str, password: str, group: str):
    pass


@app.post("/login", response_model=ResOperationMsg)
def login(user_name: str, password: str):
    pass
    # 用户不存在 or 密码错误
    # 登录成功


@app.post("/logout", response_model=ResOperationMsg)
def logout():
    pass
