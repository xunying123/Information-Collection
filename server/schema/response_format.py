from typing import Generic, Literal, TypeVar

# from common.models import *
from pydantic import (
    AfterValidator,
    AliasPath,
    BaseModel,
    Field,
    field_validator,
)
from datetime import datetime

_T = TypeVar("_T")


class ConfigBaseModel(BaseModel):
    model_config = {"from_attributes": True}


class SessionToken(ConfigBaseModel):
    access_token: str
    token_type: Literal["Bearer"]


class Category(ConfigBaseModel):
    id: int | None = None
    name: str


class IncludedCategory:
    cate_id: int
    cate_name: str | None = Field(
        validation_alias=AliasPath("category", "name"), default=None
    )


class IncludeSite:
    site_id: int
    site: str = Field(validation_alias=AliasPath("site", "name"))
    site_icon: str | None = Field(validation_alias=AliasPath("site", "icon"))


class PageItem(ConfigBaseModel, IncludedCategory, IncludeSite):
    id: int
    source_url: str
    title: str
    content: str
    publish_time: datetime = Field(alias="publish_time")

    @field_validator("content", mode="after")
    @classmethod
    def truncate(cls, v: str):
        return v[:50]


class SiteItem(ConfigBaseModel, IncludedCategory):
    id: int | None = None
    name: str
    url: str | list[str] | None
    icon: str | None = None


class Site(SiteItem):
    pages: list[PageItem]


class Keyword(ConfigBaseModel):
    id: int
    word: str
    subject: str


class Page(PageItem):
    full_content: str
    keywords: list[Keyword]


class OperationMsg(ConfigBaseModel):
    status: int = 200
    message: str = "success"


class Group(ConfigBaseModel):
    id: int
    name: str


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
    has_next: bool = None
    data: list[_T] = Field(default_factory=list)
