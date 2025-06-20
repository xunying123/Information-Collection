from fastapi import APIRouter
from fastapi import APIRouter
from server.manager.group import group_required, current_group
from .. import schema

router = APIRouter()


@router.get("/subjects", response_model=list[schema.Subject])
@group_required
def get_subjects():
    return current_group.subjects

