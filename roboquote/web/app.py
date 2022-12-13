"""Declare and configure the starlette app."""

from typing import Any
from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles
from starlette.exceptions import HTTPException
from starlette.responses import Response, JSONResponse

from roboquote import config
from roboquote.web.routes import generate, health, index


async def http_exception(request: Any, exc: Exception) -> Response:
    return JSONResponse(
        {"error": str(exc)},
        status_code=exc.status_code if hasattr(exc, "status_code") else 500,
    )


exception_handlers = {
    HTTPException: http_exception,
    500: http_exception,  # 500 are handled separately by starlette
}

app = Starlette(
    debug=config.DEBUG,
    routes=[
        index.route,
        Mount("/static", app=StaticFiles(directory="static"), name="static"),
        Mount("/health", routes=health.routes, name="health"),
        Mount("/generate", routes=generate.routes, name="generate"),
    ],
    exception_handlers=exception_handlers,
)
