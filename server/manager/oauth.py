from functools import partial
from typing import Annotated, Literal
from fastapi import HTTPException
from httpx import AsyncClient
import jwt
from pydantic import BaseModel, BeforeValidator, validate_call
from sqlalchemy import select
from common.models import User, Group
from .user import UserManager
from .db import db


class JaccountToken(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["Bearer"]
    expires_in: int


@validate_call
async def jaccount_from_token(token: JaccountToken):
    async with AsyncClient(
        headers={"Authorization": f"Bearer {token.access_token}"}
    ) as client:
        res = await client.get("https://api.sjtu.edu.cn/v1/me/profile")
    if res.status_code != 200:
        raise HTTPException(400, "Auth failed: did not get user profile from jaccount")
    profile = res.json()
    entity = profile.get("entities")[0]
    ja_code = entity.get("code")
    user = UserManager.get_user_by_jaccount_code(ja_code)
    if user is not None:
        user.username = entity.get("account")
        user.userType = entity.get("userType")
        user.name = entity.get("name")
        user.organization = entity.get("organize").get("name")
        user.avatars = entity.get("accountPhotoUrl")
    else:
        user = User(
            jaccount_code=ja_code,
            username=entity.get("account"),
            userType=entity.get("userType"),
            name=entity.get("name"),
            organization=entity.get("organize").get("name"),
            avatars=entity.get("accountPhotoUrl"),
        )
        db.add(user)
    db.flush()
    return user


class CnaesJWT(BaseModel):
    loginName: str
    name: str
    userType: str
    userName: str
    account: str
    email: str
    userCode: str
    deptCode: str


class CnaesToken(BaseModel):
    access_token: str
    refresh_token: str
    scope: str
    id_token: Annotated[
        CnaesJWT,
        BeforeValidator(
            partial(jwt.decode, options={"verify_signature": False}),
        ),
    ]
    token_type: Literal["Bearer"]
    expires_in: int


def get_cnaex_group_id():
    group_id = db.scalar(select(Group.id).where(Group.name == "中国教育科学研究院"))
    if group_id:
        return group_id
    group = Group(
        name="中国教育科学研究院",
        logo="https://www.cnaes.edu.cn/assets/images/logo_white.png",
        background="https://www.cnaes.edu.cn/assets/images/menu-bg.jpg",
        sidebar_show_mode="subject",
    )
    db.add(group)
    db.flush()
    return group.id


@validate_call
def cnaes_from_token(token: CnaesToken):
    group_id = get_cnaex_group_id()
    user = UserManager.get_user_by_cnaes_code(token.id_token.userCode)
    if user:
        user.group_id = group_id
        user.group_accepted = True
        return user
    user = User(
        cnaes_code=token.id_token.userCode,
        username=token.id_token.userName,
        userType=token.id_token.userType,
        name=token.id_token.name,
        group_id=group_id,
        group_accepted=True,
    )
    db.add(user)
    db.flush()
    return user
