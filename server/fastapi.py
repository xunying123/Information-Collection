from fastapi import Depends, FastAPI
from sqlalchemy import select
from common.models import *
from server.request_format import *
from server.request_format import SitePost
from .db import use_db, Session
from .response_format import *

app = FastAPI(root_path="/api")

@app.get("/page", response_model=PageGet)
def search_page(page_get: PageGet):
    return {"page_get": page_get}


@app.get("/category", response_model=list[ResCategory])
def get_category(db: Session = Depends(use_db)):
    stmt = select(Category).order_by(Category.id)
    res = db.scalars(stmt).all()
    return res

@app.get("/catagory/{cate_id}", response_model=ResCategory)
def get_category(cate_id: int):
    pass

@app.get("/site", response_model=list[ResSiteItem])
def get_site(subscribe: bool = False):
    pass

@app.get("/site/{site_id}", response_model=ResSite)
def get_site(site_id: int, db: Session = Depends(use_db)):
    stmt = select(Site).filter(Site.id == site_id)
    res = db.scalar(stmt)
    return res

@app.post("/site", response_model=ResOperationMsg)
def add_site(name: str, url: str, category: int, icon: str):
    ...

@app.delete("/site{site_id}", response_model=ResOperationMsg)
def delete_site(site_id: int):
    ...

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
    category: int | list[int] | None = None
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