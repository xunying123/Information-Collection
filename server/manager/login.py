# from flask_login import LoginManager, UserMixin, current_user
from fastapi import Depends
from sqlalchemy import select
from common.models import User
from fastapi_login import LoginManager
from .. import config
from .db import db
from ..utils.globalize import Globalize

login_manager = LoginManager(
    config.AppConfig.secret_key, token_url="/login", use_cookie=True
)


@login_manager.user_loader
def load_user(user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return db.scalar(stmt)


async def _get_current_user(user: User | None = Depends(login_manager.optional)):
    user = db.scalar(select(User).where(User.id == 1))
    yield user


current_user: User | Globalize[User] = Globalize[User]("current_user", _get_current_user)
