from fastapi import Depends, FastAPI
from fastapi.responses import RedirectResponse
from .manager.db import db
from .manager.user import current_user
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


@app.get("/", include_in_schema=False)
def redircet_to_docs():
    return RedirectResponse(url="/docs")
