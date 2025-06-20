from collections.abc import Sequence
from typing import Generic, Literal, TypeVar

# from common.models import *
from pydantic import (
    AliasPath,
    BaseModel,
    Field,
    TypeAdapter,
    computed_field,
    field_validator,
)
from datetime import datetime

from pydantic_core import Url
from server.manager.category import CategoryManager

_T = TypeVar("_T")


class ConfigBaseModel(BaseModel):
    model_config = {"from_attributes": True}


class CategoryItem(ConfigBaseModel):
    id: int | None = None
    name: str
    subject_id: int | None = Field(
        None, description="this is used for hint which subject is corresponding to"
    )


class Category(CategoryItem):
    @computed_field
    @property
    def sites(self) -> Sequence["SiteItem"]:
        return TypeAdapter(Sequence[SiteItem]).validate_python(
            CategoryManager.get_category_sites(self.id)
        )


class IncludedCategory:
    cate_id: int
    cate_name: str | None = Field(
        validation_alias=AliasPath("category", "name"), default=None
    )


class IncludeSite:
    site_id: int
    site: str = Field(validation_alias=AliasPath("site", "name"))
    site_icon: str | None = Field(validation_alias=AliasPath("site", "icon"))


class Keyword(ConfigBaseModel):
    id: int
    word: str


class PageItem(ConfigBaseModel, IncludeSite):
    id: int
    source_url: str
    title: str
    # to make frontend show properly when sort by time
    publish_time: datetime = Field(validation_alias=AliasPath("created_at"))
    score: int
    keywords: list[Keyword]


class SiteItem(ConfigBaseModel):
    id: int | None = None
    name: str
    url: str | list[str] | None
    icon: str | None = None


class Site(SiteItem):
    # pages: list[PageItem]
    pass


class Page(PageItem):
    full_content: str
    content: str

    @field_validator("content", mode="after")
    @classmethod
    def truncate(cls, v: str):
        return v[:50] if cls is PageItem else v


class OperationMsg(ConfigBaseModel):
    status: int = 200
    message: str = "success"


class Group(ConfigBaseModel):
    id: int
    name: str
    logo: Url | None = None
    background: str | None = None
    sidebar_show_mode: Literal["category", "subject"] = "category"


class User(ConfigBaseModel):
    id: int
    name: str
    username: str
    jaccount_code: str | None = None
    userType: str | None = None
    organization: str | None = None
    is_admin: bool = False
    avatars: str | None = None
    group: Group | None = None
    group_accepted: bool = False


class LoginStatus(ConfigBaseModel):
    is_login: bool
    user: User | None = None


class PagedQuery(ConfigBaseModel, Generic[_T]):
    cursor_id: int | None = None
    has_next: bool | None = None
    data: Sequence[_T] = Field(default_factory=Sequence[_T])


class Subject(ConfigBaseModel):
    id: int
    name: str
    keywords: list[Keyword]
