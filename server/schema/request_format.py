from pydantic import BaseModel, Field
from server.config import AppConfig
from datetime import datetime
from enum import StrEnum


class SortType(StrEnum):
    time = "time"
    score = "score"


class PageGet(BaseModel):
    site: int | None = None
    today: bool = False
    bookmarked: bool = False
    filter_user_keyword: bool = False
    subscribe: int = 0  # 0: all, 1: subscribe, -1: unsubscribe
    category: int | list[int] | None = None
    subject: int | list[int] | None = None

    time_start: datetime | None = None
    time_end: datetime | None = None

    search_title: str | None = None
    search_content: str | None = None

    count: int = AppConfig.default_paging_size
    cursor_id: int = 0  # zero should be ignored
    count_for_each_site: bool = Field(
        False,
        description="get count pages for each site and concat without further sort",
    )

    sort: SortType = SortType.time


class SitePost(BaseModel): ...


__all__ = ["PageGet", "SortType"]
