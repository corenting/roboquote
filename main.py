"""Main CLI entrypoint."""
import sys

import typer
from loguru import logger

from roboquote import config
from roboquote.background_picture import (
    get_random_background_from_unsplash_by_theme,
    get_random_background_search_query,
)
from roboquote.entities.generation_options import GenerationOptions
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
    background: str = typer.Option(
        default=None,
        help="If specified, use this string as the search query for the background picture instead of a random one. Works best with simple queries like 'mountain', 'sea' etc.",
    ),
) -> None:
    """Generate a new picture with the given filename."""
    # Get a random background category if not specified
    if background is None:
        background = get_random_background_search_query()

    # Get background to use
    background_image = get_random_background_from_unsplash_by_theme(background)

    # Get text to use
    text = get_random_quote(background)
    generate_picture(
        GenerationOptions(
            text=text,
            output_filename=filename,
            background_image=background_image,
            blur=blur,
            blur_intensity=blur_intensity,
        )
    )


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level=config.LOG_LEVEL)
    app()
