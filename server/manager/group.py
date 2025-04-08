from http.client import NOT_FOUND
from fastapi import Depends, HTTPException
from fastapi_decorators import depends
from sqlalchemy import select
from common.models import Group, User
from server.manager.user import login_manager
from server.utils.globalize import Globalize
from .db import db


class GroupManager:
    @staticmethod
    def get_group_from_id(group_id: int) -> Group:
        group = db.scalar(select(Group).where(Group.id == group_id))
        if not group:
            raise HTTPException(NOT_FOUND, "group not found")
        return group

    @staticmethod
    def get_current_group(user: User = Depends(login_manager)) -> Group | None:
        return user.group if user.group_id and user.group_accepted else None

    @staticmethod
    def get_current_group_no_accept(
        user: User = Depends(login_manager),
    ) -> Group | None:
        return user.group if user.group_id else None


current_group: Group | Globalize[Group] = Globalize[Group](
    "current_group", GroupManager.get_current_group
)


@depends
def group_required(
    group: Group | None = Depends(current_group.app_dependency),
) -> Group:
    if group is None:
        raise HTTPException(NOT_FOUND, "group not found")
    return group


@depends
def group_admin_required(
    user: User = Depends(login_manager),
    group: Group | None = Depends(current_group.app_dependency),
) -> Group:
    if group is None or not (user.group_admin or user.is_admin):
        raise HTTPException(NOT_FOUND, "group not found or not admin")
    return group


__all__ = ["GroupManager"]
