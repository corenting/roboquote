"""Main CLI entrypoint."""
import sys
from typing import Optional

import typer
from loguru import logger

from roboquote import config
from roboquote.background_image import (
    get_random_background_from_unsplash_by_theme,
    get_random_background_search_query,
)
from roboquote.entities.generate_options import GenerateOptions
from roboquote.quote_text_generation import get_random_quote
from roboquote.result_image import generate_image

app = typer.Typer()


@app.command()
def generate(
    filename: str,
    blur: bool = typer.Option(True, help="Add a blur on the background."),
    blur_intensity: Optional[int] = typer.Option(
        None, help="If blur is enabled,the blur intensity level."
    ),
    background: Optional[str] = typer.Option(
        default=None,
        help="If specified, use this string as the search query for the background image instead of a random one. Works best with simple queries like 'mountain', 'sea' etc.",
    ),
) -> None:
    """Generate a new image with the given filename."""
    # Get a random background category if not specified
    if background is None:
        background = get_random_background_search_query()

    # Get background to use
    (
        background_img,
        background_img_credits,
    ) = get_random_background_from_unsplash_by_theme(background)

    # Print credits
    print(
        f"Background by {background_img_credits.first_name} {background_img_credits.last_name} (@{background_img_credits.username}): {background_img_credits.url}"
    )

    # Get text to use
    text = get_random_quote(background)

    # Generate and save image
    generated_image = generate_image(
        GenerateOptions(
            text=text,
            background_image=background_img,
            blur=blur,
            blur_intensity=blur_intensity,
        )
    )
    generated_image.save(filename)

    print(f"Image saved as {filename}")


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stderr, level=config.LOG_LEVEL)
    app()
