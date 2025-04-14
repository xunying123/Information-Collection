from fastapi import APIRouter
from fastapi import APIRouter
from server.manager.group import group_required, current_group
from .. import schema

router = APIRouter()


@router.get("/subjects")
@group_required
def get_subjects() -> list[schema.Subject]:
    return current_group.subjects

