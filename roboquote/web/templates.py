"""Declare the Jinja2 templates for the web app."""

from starlette.templating import Jinja2Templates

from roboquote import __version__
from roboquote.constants import (
    AVAILABLE_LARGE_LANGUAGE_MODELS_NAMES,
    DEFAULT_LARGE_LANGUAGE_MODEL,
)

templates = Jinja2Templates(directory="web_templates")

# Add global informations to env
templates.env.globals["global"] = {
    "app_version": __version__,
    "default_text_model_name_for_web_ui": DEFAULT_LARGE_LANGUAGE_MODEL.name,
    "available_text_models_names": AVAILABLE_LARGE_LANGUAGE_MODELS_NAMES,
}
