from datetime import timedelta
from http.client import PRECONDITION_FAILED
from sqlalchemy import select
from common.models import User, Group
from fastapi import HTTPException, Response
from fastapi_decorators import depends
from fastapi_login import LoginManager
from server import config, schema
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
    def make_login_response(user: User, response: Response) -> schema.SessionToken:
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
        return {"access_token": token, "token_type": "Bearer"}

    @staticmethod
    def create_user(data: schema.RegisterForm) -> User:
        if db.scalar(select(User.id).where(User.username == data.username)):
            raise HTTPException(PRECONDITION_FAILED, "User already exists")
        user = User(
            username=data.username,
            password=pwd_context.hash(data.password),
            name=data.name,
        )
        if data.group_id:
            group = db.get(Group, data.group_id)
            if group is None:
                raise HTTPException(PRECONDITION_FAILED, "Group not found")
            user.group = group
        db.add(user)
        db.flush()
        return user

    @staticmethod
    def leave_group(user: User):
        user.group_id = None
        user.group_accepted = False
        user.group_admin = False

    @staticmethod
    def get_user_by_jaccount_code(code: str) -> User | None:
        stmt = select(User).where(User.jaccount_code == code)
        return db.scalar(stmt)
    
    @staticmethod
    def get_user_by_cnaes_code(code: str) -> User | None:
        stmt = select(User).where((User.cnaes_code == code) | (User.username == code))
        return db.scalar(stmt)


current_user: User | Globalize[User] = Globalize[User](
    "current_user",
    login_manager.optional,
)


login_required = depends(login_manager)

__all__ = ["login_manager", "current_user", "UserManager", "login_required"]
