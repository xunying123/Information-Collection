from pydantic import BaseModel, Field
from server.config import AppConfig
from datetime import datetime


class PageGet(BaseModel):
    category: int | list[int] | None = None
    site: int | None = None
    today: bool = False
    bookmarked: bool = False
    keyword: bool = False
    subscribe: int = Field(0, description="0: ignored, 1: only subscribed, -1: remove unsubscribed")
    time_start: datetime | None = None
    time_end: datetime | None = None
    search_title: str | None = None
    search_content: str | None = None

    count: int = AppConfig.default_paging_size
    cursor_id: int = 0  # zero should be ignored


class SitePost(BaseModel):
    ...




__all__ = ['PageGet']
