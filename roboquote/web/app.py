"""Declare and configure the starlette app."""

from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.staticfiles import StaticFiles

from roboquote import config
from roboquote.web.routes import generate, health, index

app = Starlette(
    debug=config.DEBUG,
    routes=[
        index.route,
        Mount("/static", app=StaticFiles(directory="static"), name="static"),
        Mount("/health", routes=health.routes, name="health"),
        Mount("/generate", routes=generate.routes, name="generate"),
    ],
)
