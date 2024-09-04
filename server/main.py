from flask_cors import CORS
from flask import Flask, request, Response
from flask import Blueprint

from server.db import SqlSession
from sqlalchemy import select, delete

from common.models import Category, Site, Page
from server.response_format import *
import json


def jsonify(obj):
    return Response(
        json.dumps(obj, ensure_ascii=False),
        content_type="application/json; charset=utf-8",
    )


web = Blueprint("web", __name__, static_folder="static", template_folder="templates")


@web.route("/")
def index():
    return "Hello, World!"


@web.route("/category")
def get_categories():
    result: list[ResponseCategory] = []
    stmt = select(Category).order_by(Category.id)
    with SqlSession() as db:
        for cate in db.scalars(stmt):
            info = ResponseCategory(cate)
            result.append(info)
    return jsonify(result)


@web.route("/category/<int:cate_id>/sites")
def get_category_sites(cate_id):
    result: list[ResponseSiteItem] = []
    stmt = select(Site).where(Site.cate_id == cate_id).order_by(Site.id)
    with SqlSession() as db:
        for site in db.scalars(stmt):
            info = ResponseSiteItem(site)
            result.append(info)
    return jsonify(result)


@web.route("/category/<int:cate_id>/pages")
def get_category_pages(cate_id):
    count = request.args.get("count", 20, type=int)
    offset = request.args.get("offset", 0, type=int)
    stmt = (
        select(Page)
        .where(Page.cate_id == cate_id)
        .order_by(Page.created_at.desc())
        .limit(count)
        .offset(offset)
    )
    result: list[ResponsePageItem] = []
    with SqlSession() as db:
        if db.scalar(select(Category.id).where(Category.id == cate_id)) is None:
            return "Category not found", 404
        for page in db.scalars(stmt):
            info = ResponsePageItem(page)
            result.append(info)
    return jsonify(result)


@web.route("/site")
def get_sites():
    result = []
    stmt = select(Site).order_by(Site.cate_id, Site.id)
    with SqlSession() as db:
        for site in db.scalars(stmt):
            info = ResponseSiteItem(site)
            result.append(info)
    return jsonify(result)


@web.route("/site/add", methods=["POST"])
def add_site():
    data = request.json()
    name = data.get("name")
    cate_id = int(data.get("cate_id"))
    url = data.get("url")
    icon = data.get("icon")
    with SqlSession() as db:
        try:
            site = Site(name=name, url=url, cate_id=cate_id, icon=icon)
            db.add(site)
            db.flush()
            site_id = site.id
            db.commit()
        except:
            return jsonify({"code": 1, "msg": "failed to add site."})
    return jsonify({"code": 0, "msg": "ok", "site_id": site_id})


@web.route("/site/remove", methods=["POST"])
def remove_site():
    data = request.json()
    id = data.get("id")
    is_force = data.get("force")
    with SqlSession() as db:
        if (
            not is_force
            and db.scalar(select(Page.id).where(Page.site_id == id)) is not None
        ):
            return jsonify(
                {"code": 1, "msg": "there are pages in this site. set force:true."}
            )
        db.execute(delete(Site).where(Site.id == id))
        db.commit()
    return jsonify({"code": 0, "msg": "deleted"})


@web.route("/site/<int:site_id>")
def get_site_pages(site_id):
    count = request.args.get("count", -1, type=int)
    offset = request.args.get("offset", 0, type=int)
    result: list[ResponsePageItem] = []
    stmt = select(Page).where(Page.site_id == site_id).order_by(Page.created_at.desc())
    if count > 0 and offset >= 0:
        stmt = stmt.limit(count).offset(offset)

    with SqlSession() as db:
        site = db.scalar(select(Site).where(Site.id == site_id))
        if site is None:
            return "Site not found", 404
        res = ResponseSite(site)
        for page in db.scalars(stmt):
            info = ResponsePageItem(page)
            result.append(info)
        res["pages"] = result
    return jsonify(res)


@web.route("/page")
def get_pages():
    count = request.args.get("count", -1, type=int)
    offset = request.args.get("offset", 0, type=int)
    stmt = select(Page).order_by(Page.created_at.desc())
    if count > 0 and offset >= 0:
        stmt = stmt.limit(count).offset(offset)
    result: list[ResponsePageItem] = []
    with SqlSession() as db:
        for page in db.scalars(stmt):
            info = ResponsePageItem(page)
            result.append(info)
    return jsonify(result)


@web.route("/page/<int:page_id>")
def get_page(page_id):
    stmt = select(Page).where(Page.id == page_id)
    with SqlSession() as db:
        page = db.scalar(stmt)
        if page is None:
            return "Page not found", 404
        res = ResponsePage(page)
    return jsonify(res)


@web.route("/site/<int:site_id>/page", methods=["POST"])
def add_page(site_id):
    data = request.json

    title = data.get("title")
    content = data.get("content")
    source_url = data.get("source_url")
    publish_time = data.get("publish_time")
    if not all([title, content, source_url, publish_time]):
        return (
            jsonify(
                {
                    "msg": "missing field",
                    "need": ["title", "content", "source_url", "publish_time"],
                }
            ),
            400,
        )

    with SqlSession() as db:
        # check if site exists
        cate_id = db.scalar(select(Site.cate_id).where(Site.id == site_id))
        if cate_id is None:
            return "Site not found", 404
        # check if page already exists
        existed_id = db.scalar(select(Page.id).where(Page.source_url == source_url))
        if existed_id is not None:
            return jsonify(
                {
                    "status": "duplicated",
                    "page_id": existed_id,
                    "error": "this url has been added.",
                }
            )

        page = Page(
            site_id=site_id,
            title=title,
            content=content,
            source_url=source_url,
            cate_id=cate_id,
            publish_time=publish_time,  # TODO: this line may cause error
        )
        db.add(page)
        db.flush()
        page_id = page.id
        db.commit()
    response = {
        "status": "ok",
        "page_id": page_id,
    }
    return jsonify(response)


app = Flask(__name__)
app.register_blueprint(web, url_prefix="/api")

CORS(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
