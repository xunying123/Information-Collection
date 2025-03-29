from http.client import NOT_FOUND
from fastapi import HTTPException
from sqlalchemy import select
from common.models import Group
from .db import db


class GroupManager:
    @staticmethod
    def get_group_from_id(group_id: int) -> Group:
        group = db.scalar(select(Group).where(Group.id == group_id))
        if not group:
            raise HTTPException(NOT_FOUND, "group not found")
        return group


__all__ = ["GroupManager"]
