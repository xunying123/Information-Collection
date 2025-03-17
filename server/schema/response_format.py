from typing import Generic, TypeVar
from common.models import *
from pydantic import (
    AfterValidator,
    AliasPath,
    BaseModel,
    Field,
    field_validator,
)

_T = TypeVar("_T")


class ConfigBaseModel(BaseModel):
    model_config = {"from_attributes": True}


class ResCategory(ConfigBaseModel):
    id: int
    name: str


class IncludedCategory:
    cate_id: int
    cate_name: str = Field(validation_alias=AliasPath("category", "name"))


class IncludeSite:
    site_id: int
    site: str = Field(validation_alias=AliasPath("site", "name"))
    site_icon: str = Field(validation_alias=AliasPath("site", "icon"))


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


class ResSiteItem(ConfigBaseModel, IncludedCategory):
    id: int
    name: str
    url: str | None
    icon: str | None


class ResSite(ResSiteItem):
    pages: list[PageItem]


class Keyword(ConfigBaseModel):
    id: int
    word: str
    subject: str


class ResponsePage(PageItem):
    full_content: str
    keywords: list[Keyword]


class OperationMsg(ConfigBaseModel):
    status: int = 200
    message: str = "success"


class User(ConfigBaseModel):
    id: int
    name: str
    username: str
    jaccount_code: str
    userType: str
    organization: str
    is_admin: bool
    avatars: str


class LoginStatus(ConfigBaseModel):
    is_login: bool
    user: User | None = None


class PagedQuery(ConfigBaseModel, Generic[_T]):
    cursor_id: int | None = None
    has_next: bool = None
    data: list[_T] = Field(default_factory=list)
