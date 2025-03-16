# from flask_login import LoginManager, UserMixin, current_user
from http.client import UNAUTHORIZED
from flask_login import login_required
from sqlalchemy import select
from common.models import User
from fastapi import Depends, HTTPException
from fastapi.security.base import SecurityBase
from fastapi_decorators import depends
from fastapi_login import LoginManager
from server import config
from .db import db
from ..utils.globalize import Globalize
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


class UserManager:
    @staticmethod
    def authorize(user: User | None, plain_password: str):
        if user is None:
            return False
        if not pwd_context.verify(plain_password, user.password):
            return False
        return True

    @staticmethod
    def get_user_by_id(user_id: int | str) -> User | None:
        user_id = int(user_id)
        stmt = select(User).where(User.id == user_id)
        return db.scalar(stmt)

    @staticmethod
    def get_user_by_username(username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return db.scalar(stmt)

    @staticmethod
    def set_password(user: User, password: str):
        user.password = pwd_context.hash(password)


login_manager = LoginManager(
    config.AppConfig.secret_key,
    token_url="/login",
    use_cookie=True,
    cookie_name="dic-session",
)

login_manager.user_loader()(UserManager.get_user_by_id)

current_user: User | Globalize[User] = Globalize[User](
    "current_user",
    login_manager.optional,
)


login_required = depends(login_manager)

__all__ = ["login_manager", "current_user", "UserManager", "login_required"]
