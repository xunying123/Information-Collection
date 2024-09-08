from flask_cors import CORS
from flask import Flask, request, url_for, redirect
from flask import Blueprint

from server.db import SqlSession
from sqlalchemy import select, delete

from common.models import Category, Site, Page, User
from server.response_format import *

import requests
from requests.auth import HTTPBasicAuth
from server.config import JAccountAuth, AppConfig

from flask_login import login_user, login_required, logout_user, current_user
from server.login import login_manager, User4login, admin_required
from server.utils import jsonify
from hashlib import sha256

current_user: User4login

web = Blueprint("web", __name__, static_folder="static", template_folder="templates")


@web.route("/")
def index():
    return "Hello, World!"


@web.route("/category")
@login_required
def get_categories():
    result: list[ResponseCategory] = []
    stmt = select(Category).order_by(Category.id)
    with SqlSession() as db:
        for cate in db.scalars(stmt):
            info = ResponseCategory(cate)
            result.append(info)
    return jsonify(result)


@web.route("/category/<int:cate_id>/sites")
@login_required
def get_category_sites(cate_id):
    result: list[ResponseSiteItem] = []
    stmt = select(Site).where(Site.cate_id == cate_id).order_by(Site.id)
    with SqlSession() as db:
        for site in db.scalars(stmt):
            info = ResponseSiteItem(site)
            result.append(info)
    return jsonify(result)


@web.route("/category/<int:cate_id>/pages")
@login_required
def get_category_pages(cate_id):
    count = request.args.get("count", AppConfig.default_paging_size, type=int)
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
@login_required
def get_sites():
    result = []
    stmt = select(Site).order_by(Site.cate_id, Site.id)
    with SqlSession() as db:
        for site in db.scalars(stmt):
            info = ResponseSiteItem(site)
            result.append(info)
    return jsonify(result)


@web.route("/site/add", methods=["POST"])
@login_required
@admin_required
def add_site():
    data = request.json
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
@login_required
@admin_required
def remove_site():
    data = request.json
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
@login_required
def get_site_pages(site_id):
    count = request.args.get("count", AppConfig.default_paging_size, type=int)
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
@login_required
def get_pages():
    count = request.args.get("count", AppConfig.default_paging_size, type=int)
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
@login_required
def get_page(page_id):
    stmt = select(Page).where(Page.id == page_id)
    with SqlSession() as db:
        page = db.scalar(stmt)
        if page is None:
            return "Page not found", 404
        res = ResponsePage(page)
    return jsonify(res)


@web.route("/page/search")
@login_required
def search_page():
    key = request.args.get("key", type=str)
    count = request.args.get("count", AppConfig.default_paging_size, type=int)
    offset = request.args.get("offset", 0, type=int)
    if not key:
        return jsonify({"code": 1, "msg": "missing key"})
    stmt = (
        select(Page)
        .where(Page.title.like(f"%{key}%"))
        .order_by(Page.created_at.desc())
        .limit(count)
        .offset(offset)
    )
    result: list[ResponsePageItem] = []
    with SqlSession() as db:
        for page in db.scalars(stmt):
            info = ResponsePageItem(page)
            result.append(info)
    return jsonify(result)


@web.route("/site/<int:site_id>/page", methods=["POST"])
@login_required
@admin_required
def add_page(site_id):
    data = request.json

    title = data.get("title")
    content = data.get("content")
    full_content = data.get("full_content")
    source_url = data.get("source_url")
    publish_time = data.get("publish_time")
    if not all([title, content, source_url, publish_time, full_content]):
        return (
            jsonify(
                {
                    "msg": "missing field",
                    "need": [
                        "title",
                        "content",
                        "source_url",
                        "publish_time",
                        "full_content",
                    ],
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
            full_content=full_content,
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


@web.route("/auth")
def do_auth_callback():
    try:
        code = request.args.get("code")
        state = request.args.get("state")
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": url_for("web.do_auth_callback", _external=True),
            "client_id": JAccountAuth.client_id,
            "client_secret": JAccountAuth.secretkey,
        }
        response = requests.post(
            "https://jaccount.sjtu.edu.cn/oauth2/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data,
            auth=HTTPBasicAuth("czZCaGRSa3F0MzpnWDFmQmF0M2JW", ""),
        )
        print(f"{response.json()=}")
        access_token: str = response.json().get("access_token")
        print(f"{access_token=}")
        profile = requests.get(
            "https://api.sjtu.edu.cn/v1/me/profile",
            headers={"Authorization": f"Bearer {access_token}"},
        ).json()
        entity = profile.get("entities")[0]

        print("get entity success")
        print(entity)
        code = entity.get("code")
        print(f"{code=}")
        with SqlSession() as db:
            user = db.scalar(select(User).where(User.jaccount_code == code))
            if user is None:
                user = User(
                    jaccount_code=code,
                    username=entity.get("account"),
                    userType=entity.get("userType"),
                    name=entity.get("name"),
                    organization=entity.get("organize").get("name"),
                    is_admin=False,
                    avatars=entity.get("accountPhotoUrl"),
                )
                db.add(user)
            else:
                user.username = entity.get("account")
                user.userType = entity.get("userType")
                user.name = entity.get("name")
                user.organization = entity.get("organize").get("name")
                user.avatars = entity.get("accountPhotoUrl")
            db.flush()
            db.commit()
            login_user(User4login(user), remember=True)
        return redirect(state, code=302)
    except Exception as e:
        print(f"exception: {e=}")
        return "Auth failed", 400

@web.route("login", methods=["POST"])
def do_login_with_password():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if not all([username, password]):
        return jsonify({"code": -1, "msg": "something missing"})
    with SqlSession() as db:
        user = db.scalar(select(User).where(User.username == username))
        if user is None:
            return jsonify({"code": -4, "msg": "用户不存在"})
        if user.password is None:
            return jsonify({"code": -2, "msg": "尚未设置密码"})
        [salt, hash_str] = user.password.split("-", 1)
        check_hash = sha256((salt + password).encode('utf-8')).hexdigest()
        if check_hash != hash_str:
            return jsonify({"code": -3, "msg": "密码错误"})
        login_user(User4login(user), remember=True)
    return jsonify({"code": 0, "msg": "登录成功"})


@web.route("/logout", methods=["POST"])
def do_logout():
    logout_user()
    return jsonify({"code": 0})


@web.route("/user/me")
def get_me():
    if current_user.is_authenticated:
        return jsonify({"code": 0, "user": current_user.__dict__})
    else:
        return jsonify({"code": 1, "msg": "not logged in"})


app = Flask(__name__)
app.config["SECRET_KEY"] = AppConfig.secret_key

app.register_blueprint(web, name="web", url_prefix="/api")

CORS(app)
login_manager.init_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
