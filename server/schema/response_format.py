from common.models import *
from pydantic import (
    AfterValidator,
    AliasPath,
    BaseModel,
    Field,
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
    content: str = Annotated[str, AfterValidator(lambda x: x[:50])]
    publish_time: datetime = Field(alias="publish_time")

class ResSiteItem(ConfigBaseModel, IncludedCategory):
    id: int
    name: str
    url: str | None
    icon: str | None

class ResSite(ResSiteItem):
    pages: list[ResPageItem]

class ResponseKeywordItem(ConfigBaseModel):
    id: int
    word: str
    subject: str

class ResponsePage(ResPageItem):
    full_content: str
    keywords: list[ResponseKeywordItem]

class ResOperationMsg(ConfigBaseModel):
    status: bool
    message: str
