from .user import router as user_router
from .page import router as page_router
from .subscribe import router as subscrbie_router
from .subject import router as subject_router
from .category import router as category_router

__all__ = ["user_router", "page_router", "subscrbie_router", "subject_router", "category_router"]
