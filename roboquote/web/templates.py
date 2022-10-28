"""Declare the Jinja2 templates for the web app."""
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="web_templates")
