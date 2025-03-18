from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.routing import APIRoute
from .manager.db import db
from .manager.user import current_user
from .router import *


def custom_generate_unique_id(route: APIRoute):
    prefix = f"{route.tags[0]}-" if route.tags else ""
    return f"{prefix}{route.name}"


app = FastAPI(
    root_path="/api",
    dependencies=[
        Depends(db.app_dependency),
        Depends(current_user.app_dependency),
    ],
    generate_unique_id_function=custom_generate_unique_id,
)


@app.exception_handler(Exception)
def the_least_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal Server Error",
            "detail": str(exc),
            "request": f"{request.method} {request.url}",
        },
    )


app.include_router(user_router)
app.include_router(page_router)
app.include_router(subscrbie_router)


@app.get("/", include_in_schema=False)
def redircet_to_docs():
    return RedirectResponse(url="/docs")
