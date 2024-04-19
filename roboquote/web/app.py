"""Declare and configure the starlette app."""

from typing import Any

from loguru import logger
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse, Response
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from roboquote import config
from roboquote.web.routes import generate, health, index


async def http_exception(request: Any, exc: Exception) -> Response:
    if config.WEB_DEBUG:
        logger.exception(exc)
    return JSONResponse(
        {"error": getattr(exc, "detail", str(exc))},
        status_code=getattr(exc, "status_code", 500),
    )


exception_handlers = {
    HTTPException: http_exception,
    500: http_exception,  # 500 are handled separately by starlette
}

app = Starlette(
    debug=config.WEB_DEBUG,
    routes=[
        index.route,
        Mount("/static", app=StaticFiles(directory="static"), name="static"),
        Mount("/health", routes=health.routes, name="health"),
        Mount("/generate", routes=generate.routes, name="generate"),
    ],
    exception_handlers=exception_handlers,
)
