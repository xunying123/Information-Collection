from sqlalchemy import exists
from sqlalchemy.orm import aliased
from common.models import *
from .db import db


class CategoryManager:
    @staticmethod
    def get_category_sites(category_id: int | None) -> list[Site]:
        from .user import current_user

        if category_id == 0:
            category_id = None  # for sql use

        user_id = current_user.id
        stmt = (
            select(Site)
            .outerjoin(
                CategorySiteRelation,
                (CategorySiteRelation.category_id == category_id)
                & (CategorySiteRelation.site_id == Site.id),
            )
            .outerjoin(
                UserSiteRelation,
                (UserSiteRelation.site_id == Site.id)
                & (UserSiteRelation.user_id == user_id)
                & (UserSiteRelation.category_id == category_id),
            )
            .where(
                (
                    (CategorySiteRelation.site_id != None)
                    & (
                        (UserSiteRelation.negative == None)
                        | (UserSiteRelation.negative == False)
                    )
                )
                | (UserSiteRelation.negative == False)
            )
            .distinct()
        )
        return db.scalars(stmt).all()

    def get_subscribe_category() -> Category:
        return Category(id=0, name="个人订阅")

    def get_category_by_id(id: int) -> Category:
        if id == 0:
            return CategoryManager.get_subscribe_category()
        res = db.scalar(select(Category).where(Category.id == id))
        return res
