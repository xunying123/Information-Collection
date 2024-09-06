from flask_login import LoginManager, UserMixin, current_user
from common.models import User
from server.db import SqlSession
from sqlalchemy import select
from server.utils import jsonify
from functools import wraps

login_manager = LoginManager()


class User4login(UserMixin):
    def __init__(self, user: User):
        self.id = user.id
        self.jaccount_code = user.jaccount_code
        self.username = user.username
        self.userType = user.userType
        self.name = user.name
        self.organization = user.organization
        self.is_admin = user.is_admin
        self.avatars = user.avatars


@login_manager.user_loader
def load_user(user_id):
    with SqlSession() as db:
        user = db.scalar(select(User).where(User.id == user_id))
        if user is None:
            return None
        return User4login(user)


@login_manager.unauthorized_handler
def unauthorized_handler():
    return jsonify({"error": "unauthorized. please login first."}), 401


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            return jsonify({"status": "error", "message": "Permission denied"}), 403
        return func(*args, **kwargs)

    return wrapper
