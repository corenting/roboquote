"""Main CLI entrypoint."""
import asyncio

import typer

from roboquote.background_image import (
    get_random_background_from_unsplash_by_theme,
    get_random_background_search_query,
)
from roboquote.entities.generate_options import GenerateOptions
from roboquote.entities.text_model import TextModel
from roboquote.quote_text_generation import get_random_quote
from roboquote.result_image import generate_image

app = typer.Typer()


@app.command()
def generate(
    filename: str,
    blur: bool = typer.Option(True, help="Add a blur on the background."),
    blur_intensity: int | None = typer.Option(
        None, help="If blur is enabled,the blur intensity level."
    ),
    background: str | None = typer.Option(
        default=None,
        help="If specified, use this string as the search query "
        + "for the background image instead of a random one. "
        + "Works best with simple queries like 'mountain', 'sea' etc.",
    ),
    text_model: TextModel = typer.Option(
        default=TextModel.MISTRAL_8X7B_INSTRUCT.value,
        help="The text generation model to use.",
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
    text = asyncio.run(get_random_quote(background, text_model))

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
