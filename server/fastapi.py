from fastapi import Depends, FastAPI
from sqlalchemy import select
from common.models import *
from server.request_format import *
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

@app.get("/site/{site_id}", response_model=ResSiteItem)
def get_site(site_id: int, db: Session = Depends(use_db)):
    stmt = select(Site).filter(Site.id == site_id)
    res = db.scalar(stmt)
    return res