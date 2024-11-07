from flask_cors import CORS
from flask import Flask, request, url_for, redirect, g
from flask import Blueprint

from server.db import db, Session
from sqlalchemy import select, delete, exists, func, not_

from common.models import *
from server.response_format import *

import requests
from requests.auth import HTTPBasicAuth
from server.config import JAccountAuth, AppConfig

from flask_login import login_user, login_required, logout_user, current_user
from server.login import login_manager, User4login, admin_required
from server.utils import jsonify
from hashlib import sha256
import pytz

current_user: User4login

web = Blueprint("web", __name__, static_folder="static", template_folder="templates")


@web.teardown_request
def teardown_request(exception):
    db: Session | None = g.pop("db", None)
    if db is not None:
        with db:
            if exception is None:
                db.commit()
            else:
                db.rollback()


@web.route("/")
def index():
    return "Hello, World!"


@web.route("/category")
@login_required
def get_categories():
    result: list[ResponseCategory] = []
    stmt = select(Category).order_by(Category.id)
    for cate in db.scalars(stmt):
        info = ResponseCategory(cate)
        result.append(info)
    return jsonify(result)


@web.route("/category/<int:cate_id>")
@login_required
def get_category(cate_id):
    cate = db.scalar(select(Category).where(Category.id == cate_id))
    if cate is None:
        return "Category not found", 404
    return jsonify(ResponseCategory(cate))


@web.route("/site")
@login_required
def get_sites():
    category = request.args.get("category", None, type=int)
    subscribe = request.args.get("subscribe", "false").lower() == "true"
    result = []
    stmt = select(Site).order_by(Site.cate_id, Site.id)
    if category is not None:
        stmt = stmt.where(Site.cate_id == category)
    if subscribe:
        stmt = stmt.where(
            exists().where(
                (UserSiteRelation.user_id == current_user.id)
                & (UserSiteRelation.site_id == Site.id)
            )
        )
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
    try:
        site = Site(name=name, url=url, cate_id=cate_id, icon=icon)
        db.add(site)
        db.flush()
        site_id = site.id
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
    if (
        not is_force
        and db.scalar(select(Page.id).where(Page.site_id == id)) is not None
    ):
        return jsonify(
            {"code": 1, "msg": "there are pages in this site. set force:true."}
        )
    db.execute(delete(Site).where(Site.id == id))
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

    site = db.scalar(select(Site).where(Site.id == site_id))
    if site is None:
        return "Site not found", 404
    res = ResponseSite(site)
    return jsonify(res)


@web.route("/page")
@login_required
def get_pages():
    count = request.args.get("count", AppConfig.default_paging_size, type=int)
    cursor_id = request.args.get("cursor_id", None, type=int)
    category = request.args.get("category", None, type=int)
    site = request.args.get("site", None, type=int)
    only_today = request.args.get("today", "false").lower() == "true"
    bookmarked = request.args.get("bookmarked", "false").lower() == "true"
    filterd_by_keyword = request.args.get("keyword", "false").lower() == "true"
    filterd_by_subscribe = request.args.get("subscribe", "false").lower() == "true"

    stmt = select(Page).order_by(Page.created_at.desc())

    if only_today:
        shanghai_tz = pytz.timezone("Asia/Shanghai")
        today = datetime.now(shanghai_tz).date()
        stmt = stmt.where(func.date(Page.publish_time) == today)
    if bookmarked:
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
    if cursor_id is not None:
        stmt = stmt.where(Page.id < cursor_id)
    if count > 0:
        stmt = stmt.limit(count)

    sites_id = None
    if site is not None:
        sites_id = [site]
    elif category is not None:
        # special logic: count is used to limit every SITE instead of total pages
        # cursor_id should not be used in this case CURRENTLY
        # TODO: support cursor_id in this case
        sites_id = db.scalars(select(Site.id).where(Site.cate_id == category))

    result: list[ResponsePageItem] = []

    def get_once(stmt):
        for page in db.scalars(stmt):
            info = ResponsePageItem(page)
            result.append(info)

    if sites_id is not None:
        for site_id in sites_id:
            get_once(stmt.where(Page.site_id == site_id))
    else:
        get_once(stmt)
    new_cursor_id = min([x["id"] for x in result]) if result else None
    return jsonify({"pages": result, "cursor_id": new_cursor_id})


@web.route("/page/<int:page_id>")
@login_required
def get_page(page_id):
    stmt = select(Page).where(Page.id == page_id)
    page = db.scalar(stmt)
    if page is None:
        return "Page not found", 404
    res = ResponsePage(page)
    return jsonify(res)


@web.route("/page/search")
@login_required
def search_page():
    count = request.args.get("count", AppConfig.default_paging_size, type=int)
    offset = request.args.get("offset", 0, type=int)
    key = request.args.get("key", type=str)
    site = request.args.get("site", 0, type=int)
    cate = request.args.get("cate", 0, type=int)
    time_start = request.args.get("time_start", type=str)
    time_end = request.args.get("time_end", type=str)
    if not any([key, site, cate, time_start, time_end]):
        return jsonify(
            {
                "code": 1,
                "msg": "at least one of key, site, cate, time_start, time_end is required.",
            }
        )
    stmt = select(Page).order_by(Page.created_at.desc()).limit(count).offset(offset)
    if key:
        stmt = stmt.where(Page.title.like(f"%{key}%"))
    if site:
        stmt = stmt.where(Page.site_id == site)
    if cate:
        stmt = stmt.where(Page.cate_id == cate)
    if time_start:
        stmt = stmt.where(Page.publish_time >= time_start)
    if time_end:
        stmt = stmt.where(Page.publish_time <= time_end)
    result: list[ResponsePageItem] = []
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
    user = db.scalar(select(User).where(User.username == username))
    if user is None:
        return jsonify({"code": -4, "msg": "用户不存在"})
    if user.password is None:
        return jsonify({"code": -2, "msg": "尚未设置密码"})
    [salt, hash_str] = user.password.split("-", 1)
    check_hash = sha256((salt + password).encode("utf-8")).hexdigest()
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


@web.route("/bookmark/add", methods=["POST"])
@login_required
def add_bookmark():
    data = request.json
    page_id = data.get("page_id")
    user = db.scalar(select(User).where(User.id == current_user.id))
    if user is None:
        return jsonify({"code": 1, "msg": "user not found"})
    page = db.scalar(select(Page).where(Page.id == page_id))
    if page is None:
        return jsonify({"code": 2, "msg": "page not found"})
    user.bookmarks.append(page)
    return jsonify({"code": 0, "msg": "ok"})


@web.route("/bookmark/remove", methods=["POST"])
@login_required
def remove_bookmark():
    data = request.json
    page_id = data.get("page_id")
    if page_id is None:
        return jsonify({"code": 1, "msg": "missing page_id"})
    db.execute(
        delete(Bookmark).where(
            (Bookmark.user_id == current_user.id) & (Bookmark.page_id == page_id)
        )
    )
    return jsonify({"code": 0, "msg": "ok"})


@web.route("/bookmark")
@login_required
def get_bookmarks():
    count = request.args.get("count", AppConfig.default_paging_size, type=int)
    offset = request.args.get("offset", 0, type=int)
    time_start = request.args.get("time_start", type=str)
    time_end = request.args.get("time_end", type=str)
    stmt = (
        select(Bookmark)
        .where(Bookmark.user_id == current_user.id)
        .order_by(Bookmark.created_at)
        .limit(count)
        .offset(offset)
    )
    if time_start:
        stmt = stmt.where(Bookmark.created_at >= time_start)
    if time_end:
        stmt = stmt.where(Bookmark.created_at <= time_end)

    result = []
    bookmarks = db.scalars(stmt)
    for bm in bookmarks:
        info = ResponsePageItem(bm.page)
        result.append(info)
    return jsonify(result)


@web.route("/keyword")
@login_required
def get_keywords():
    personal = request.args.get("personal", "false", type=str)
    stmt = select(Keyword)
    if personal == "true":
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
    return jsonify(result)


@web.route("/keyword", methods=["POST"])
@login_required
def add_keyword():
    data = request.json
    words = data["words"]
    add_for_user = data.get("add_for_user", True)
    keep_user_existed = data.get("keep_user_existed", True)
    if type(words) is not list:
        return jsonify({"code": 1, "msg": "invalid request: words is not an array"})
    for word in words:
        if type(word) is not str:
            return jsonify({"code": 1, "msg": "invalid request: word is not a string"})
    if add_for_user is not None and type(add_for_user) is not bool:
        return jsonify({"code": 1, "msg": "invalid request"})
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
    return jsonify({"code": 0, "msg": "ok", "keywords_id": kw_ids})


@web.route("/keyword", methods=["DELETE"])
@login_required
def remove_keyword():
    data = request.json
    keyword_id = data["keyword_id"]
    if type(keyword_id) is not int:
        return jsonify({"code": 1, "msg": "invalid request"})
    stmt = delete(UserKeywordRelation).where(
        (UserKeywordRelation.user_id == current_user.id)
        & (UserKeywordRelation.keyword_id == keyword_id)
    )
    db.execute(stmt)
    return jsonify({"code": 0, "msg": "ok"})


@web.route("/subscribe", methods=["GET"])
@login_required
def get_subscribes():
    result = []
    user = db.scalar(select(User).where(User.id == current_user.id))
    for site in user.sites:
        info = ResponseSiteItem(site)
        result.append(info)
    return jsonify({"sites": result})


@web.route("/subscribe", methods=["POST"])
@login_required
def add_subscribe():
    data = request.json
    sites_id = data.get("sites_id")
    keep_user_existed = data.get("keep_user_existed", True)
    if type(sites_id) is not list:
        return jsonify({"code": 1, "msg": "invalid request: sites_id is not an array"})
    for site_id in sites_id:
        if type(site_id) is not int:
            return jsonify(
                {"code": 1, "msg": "invalid request: site_id is not a number"}
            )
    if not keep_user_existed:
        db.execute(
            delete(UserSiteRelation).where(
                (UserSiteRelation.user_id == current_user.id)
                & (UserSiteRelation.site_id.not_in(sites_id))
            )
        )
    for site_id in sites_id:
        site = db.scalar(select(Site).where(Site.id == site_id))
        if site is None:
            return jsonify({"code": 2, "msg": "site not found: " + str(site_id)})
        if (
            db.scalar(
                select(UserSiteRelation).where(
                    (UserSiteRelation.user_id == current_user.id)
                    & (UserSiteRelation.site_id == site_id)
                )
            )
            is not None
        ):
            continue
        db.add(UserSiteRelation(user_id=current_user.id, site_id=site_id))
    return jsonify({"code": 0, "msg": "ok"})


@web.route("/subscribe", methods=["DELETE"])
@login_required
def remove_subscribe():
    data = request.json
    site_id = data.get("site_id")
    if site_id is None:
        return jsonify({"code": 1, "msg": "missing site_id"})
    db.execute(
        delete(UserSiteRelation).where(
            (UserSiteRelation.user_id == current_user.id)
            & (UserSiteRelation.site_id == site_id)
        )
    )
    return jsonify({"code": 0, "msg": "ok"})


app = Flask(__name__)
app.config["SECRET_KEY"] = AppConfig.secret_key

app.register_blueprint(web, name="web", url_prefix="/api")

CORS(app)
login_manager.init_app(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
