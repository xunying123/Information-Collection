# from flask_login import LoginManager, UserMixin, current_user
from datetime import timedelta
from flask_login import login_required
from sqlalchemy import select
from common.models import User
from fastapi import Response
from fastapi_decorators import depends
from fastapi_login import LoginManager
from server import config
from .db import db
from ..utils.globalize import Globalize
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

login_manager = LoginManager(
    config.AppConfig.secret_key,
    token_url="/login",
    use_cookie=True,
    cookie_name="dic-session",
)


class UserManager:
    @staticmethod
    def authorize(user: User | None, plain_password: str):
        if user is None:
            return False
        if not pwd_context.verify(plain_password, user.password):
            return False
        return True

    @login_manager.user_loader()
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

    @staticmethod
    def make_login_response(user: User, response: Response):
        expiration = timedelta(days=7)
        # the sub must be a string
        token = login_manager.create_access_token(
            data={"sub": str(user.id)}, expires=expiration
        )
        response.set_cookie(
            key=login_manager.cookie_name,
            value=token,
            httponly=True,
            samesite="lax",
            max_age=expiration,
        )
        return {"access_token": token, "token_type": "bearer"}


current_user: User | Globalize[User] = Globalize[User](
    "current_user",
    login_manager.optional,
)


login_required = depends(login_manager)

__all__ = ["login_manager", "current_user", "UserManager", "login_required"]
