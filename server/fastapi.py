from fastapi import Depends, FastAPI
from sqlalchemy import select
from common.models import *
from server.request_format import *
from server.request_format import SitePost
from .db import use_db, Session
from .response_format import *

app = FastAPI()

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
    ...

@app.get("/site", response_model=list[ResSiteItem])
def get_site():
    ...

@app.get("/site/{site_id}", response_model=ResSiteItem)
def get_site(site_id: int, db: Session = Depends(use_db)):
    stmt = select(Site).filter(Site.id == site_id)
    res = db.scalar(stmt)
    return res

@app.post("/site", response_model=ResSiteItem)
def add_site(site_post: SitePost):
    ...

@app.delete("/site", response_class=ResOperationMsg)
def delete_site(site_id: int):
    ...

