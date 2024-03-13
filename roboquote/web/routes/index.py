"""Handle the index route."""

from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from roboquote.web.templates import templates


async def index(request: Request) -> Response:
    """Index route to display the main page."""
    return templates.TemplateResponse("index.html", {"request": request})


route = Route("/", endpoint=index)
