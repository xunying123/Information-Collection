from pydantic import BaseModel
from server.config import AppConfig

class PageGet(BaseModel):
    category: int | list[int] | None = None
    site: int | None = None
    today: bool = False
    bookmarked: bool = False
    keyword: bool = False
    subscribe: bool = False
    count: int = AppConfig.default_paging_size
    cursor_id: int = None


__all__ = [PageGet]
