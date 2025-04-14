from http.client import PRECONDITION_FAILED
from fastapi import APIRouter, HTTPException, Body
from sqlalchemy import select, delete
from common.models import *
from server import schema
from server.manager.category import CategoryManager
from ..manager.user import login_required
from ..manager.db import db
from ..manager.group import current_group, group_admin_required, group_required

router = APIRouter()


@router.get("/category")
@group_required
def get_categories() -> list[schema.Category]:
    res = list(current_group.categories)
    res.append(CategoryManager.get_subscribe_category())
    return res


@router.get("/category/{cate_id}", response_model=schema.Category)
@login_required
def get_category(cate_id: int):
    return CategoryManager.get_category_by_id(cate_id)


@router.post("/category", response_model=schema.OperationMsg)
@group_admin_required
def add_category(category: schema.CategoryItem):
    if (
        db.scalar(
            select(Category.id).where(
                Category.name == category.name
                and Category.belonged_group_id == current_group.id
            )
        )
        is not None
    ):
        raise HTTPException(PRECONDITION_FAILED, "category already exists")
    cate = Category(name=category.name, belonged_group_id=current_group.id)
    db.add(cate)
    return {}


@router.post("/category/site", response_model=schema.OperationMsg)
@group_admin_required
def add_site_to_category(cate_id: int = Body(), site_id: int = Body()):
    if (
        db.scalar(select(Category.belonged_group_id).where(Category.id == cate_id))
        != current_group.id
    ):
        raise HTTPException(PRECONDITION_FAILED, "category not in current group")
    if (
        db.scalar(
            select(CategorySiteRelation)
            .where(CategorySiteRelation.category_id == cate_id)
            .where(CategorySiteRelation.site_id == site_id)
        )
        is not None
    ):
        return schema.OperationMsg(message="site already added into this category")
    rel = CategorySiteRelation(site_id=site_id, category_id=cate_id)
    db.add(rel)
    return {}


@router.delete("/category/site", response_model=schema.OperationMsg)
@group_admin_required
def remove_site_from_category(cate_id: int = Body(), site_id: int = Body()):
    if (
        db.scalar(select(Category.belonged_group_id).where(Category.id == cate_id))
        != current_group.id
    ):
        raise HTTPException(PRECONDITION_FAILED, "category not in current group")
    stmt = (
        delete(CategorySiteRelation)
        .where(CategorySiteRelation.category_id == cate_id)
        .where(CategorySiteRelation.site_id == site_id)
    )
    db.execute(stmt)
    return {}
