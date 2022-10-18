"""Main CLI entrypoint."""
import sys

import typer
from loguru import logger

from roboquote import config
from roboquote.background_picture import get_random_background_theme
from roboquote.entities.generation_options import GenerationOptions
from roboquote.entities.themes import Theme
from roboquote.quote_text_generation import get_random_quote
from roboquote.result_picture import generate_picture

app = typer.Typer()


@app.command()
def generate(
    filename: str,
    blur: bool = typer.Option(True, help="Add a blur on the background."),
    blur_intensity: int = typer.Option(
        5, help="If blur is enabled,the blur intensity level."
    ),
    background_theme: Theme = typer.Option(
        default=None,
        help="If specified, use this theme for the background picture instead of a random one.",
    ),
    # handpicked_background: bool = typer.Option(
    #    True,
    #    help="If enabled, use an handpicked background picture instead of a random one from Internet.",
    # ),
) -> None:
    """Generate a new picture with the given filename."""
    # Get a random background category if not specified
    if background_theme is None:
        background_theme = get_random_background_theme()

    # Get text to use
    text = get_random_quote(background_theme)
    generate_picture(
        GenerationOptions(
            text=text,
            filename=filename,
            background_theme=background_theme,
            blur=blur,
            blur_intensity=blur_intensity,
        )
    )


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level=config.LOG_LEVEL)
    app()
