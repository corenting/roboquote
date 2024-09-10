"""Main CLI entrypoint."""

import asyncio
from typing import Annotated

import click
import typer

from roboquote.background_image import (
    get_random_background_from_unsplash_by_theme,
    get_random_background_search_query,
)
from roboquote.constants import (
    AVAILABLE_LARGE_LANGUAGE_MODELS,
    AVAILABLE_LARGE_LANGUAGE_MODELS_NAMES,
    DEFAULT_LARGE_LANGUAGE_MODEL,
)
from roboquote.entities.generate_options import GenerateOptions
from roboquote.quote_text_generation import get_random_quote
from roboquote.result_image import generate_image

app = typer.Typer()


@app.command()
def generate(
    filename: str,
    blur: Annotated[bool, typer.Option(help="Add a blur on the background.")] = True,
    blur_intensity: Annotated[
        int | None, typer.Option(help="If blur is enabled,the blur intensity level.")
    ] = None,
    background: Annotated[
        str | None,
        typer.Option(
            help="If specified, use this string as the search query "
            + "for the background image instead of a random one. "
            + "Works best with simple queries like 'mountain', 'sea' etc.",
        ),
    ] = None,
    model_name: Annotated[
        str,
        typer.Option(
            click_type=click.Choice(AVAILABLE_LARGE_LANGUAGE_MODELS_NAMES),
            help="The name of the LLM to use for the text generation.",
        ),
    ] = DEFAULT_LARGE_LANGUAGE_MODEL.name,
) -> None:
    """Generate a new image with the given filename."""
    # Get model
    large_language_model = next(
        model for model in AVAILABLE_LARGE_LANGUAGE_MODELS if model.name == model_name
    )

    # Get a random background category if not specified
    if background is None:
        background = get_random_background_search_query()

    # Get background to use
    (
        background_img,
        background_img_credits,
    ) = asyncio.run(get_random_background_from_unsplash_by_theme(background))

    # Print credits
    print(
        "Background by "
        + background_img_credits.first_name
        + " "
        + background_img_credits.last_name
        + f" (@{background_img_credits.username}): {background_img_credits.url}"
    )

    # Get text to use
    text = asyncio.run(get_random_quote(background, large_language_model))

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
    app()
