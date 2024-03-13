"""Handle health-related routes."""

from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route


async def ping(request: Request) -> Response:
    """Handle ping endpoint."""
    return JSONResponse({"ping": "pong"})


routes = [
    Route("/ping", endpoint=ping),
]
