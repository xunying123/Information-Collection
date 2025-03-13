from pydantic import BaseModel
from server.config import AppConfig
from datetime import datetime


class PageGet(BaseModel):
    category: int | list[int] | None = None
    site: int | None = None
    today: bool = False
    bookmarked: bool = False
    keyword: bool = False
    subscribe: bool = False
    time_start: datetime | None = None
    time_end: datetime | None = None
    search_title: str | None = None
    search_content: str | None = None

    count: int = AppConfig.default_paging_size
    cursor_id: int = 0  # zero should be ignored


__all__ = ['PageGet']
