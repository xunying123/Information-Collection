from common.models import *
from pydantic import (
    AfterValidator,
    AliasPath,
    BaseModel,
    Field,
    field_validator,
)


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


class ResPageItem(ConfigBaseModel, IncludedCategory, IncludeSite):
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
    pages: list[ResPageItem]


class Keyword(ConfigBaseModel):
    id: int
    word: str
    subject: str


class ResponsePage(ResPageItem):
    full_content: str
    keywords: list[Keyword]


class OperationMsg(ConfigBaseModel):
    status: int = 200
    message: str = "success"


class UserInfo(ConfigBaseModel):
    id: int
    name: str
    username: str
    jaccount_code: str
    userType: str
    organization: str
    is_admin: bool
    avatars: str
