from fastapi import Depends, FastAPI
import pytz
from sqlalchemy import exists, or_, select, and_, delete
from common.models import *
from server.schema.request_format import *
from .schema.response_format import *
from .manager.db import db
from .manager.login import current_user
from .router import user_router, page_router

app = FastAPI(
    root_path="/api",
    dependencies=[
        Depends(db.app_dependency),
        Depends(current_user.app_dependency),
    ],
)

app.include_router(user_router)
app.include_router(page_router)

