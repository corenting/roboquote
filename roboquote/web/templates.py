"""Declare the Jinja2 templates for the web app."""
from starlette.templating import Jinja2Templates

from roboquote import __version__
from roboquote.constants import DEFAULT_WEB_TEXT_MODEL
from roboquote.entities.text_model import TextModel

templates = Jinja2Templates(directory="web_templates")

# Add global informations to env
templates.env.globals["global"] = {
    "app_version": __version__,
    "default_text_model_name_for_web_ui": DEFAULT_WEB_TEXT_MODEL.value,
    "available_text_models_names": [i.value for i in TextModel],
}
