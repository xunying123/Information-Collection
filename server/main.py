from flask import Flask, request
from flask import Blueprint

from server.db import SqlSession
from sqlalchemy import select

from common.models import Category, Site, Page

import json

web = Blueprint("web", __name__, static_folder="static", template_folder="templates")


@web.route("/")
def index():
    return "Hello, World!"


@web.route("/site")
def get_sites():
    result = []
    stmt = select(Site).order_by(Site.cate_id, Site.id)
    with SqlSession() as db:
        for source in db.scalars(stmt):
            info = {
                "id": source.id,  # used for query
                "name": source.name,
                "url": source.url,
                "catagory": source.category.name,
            }
            result.append(info)
    return json.dumps(result, ensure_ascii=False)


@web.route("/site/<int:site_id>")
def get_site_pages(site_id):
    count = request.args.get("count", 20, type=int)
    offset = request.args.get("offset", 0, type=int)
    result = []
    stmt = (
        select(Page)
        .where(Page.site_id == site_id)
        .order_by(Page.created_at.desc())
        .limit(count)
        .offset(offset)
    )
    with SqlSession() as db:
        for page in db.scalars(stmt):
            info = {
                "id": page.id,
                "title": page.title,
                "content": page.content,
                "source_url": page.source_url,
            }
            result.append(info)
    return json.dumps(result, ensure_ascii=False)


@web.route("/page/<int:page_id>")
def get_page(page_id):
    stmt = select(Page).where(Page.id == page_id)
    with SqlSession() as db:
        page = db.scalar(stmt)
        if page is None:
            return "Page not found", 404
        res = {
            "title": page.title,
            "content": page.content,
            "source_url": page.source_url,
        }
    return json.dumps(res, ensure_ascii=False)


app = Flask(__name__)
app.register_blueprint(web)

app.run(host="0.0.0.0", port=5000, debug=True)
