"""Main CLI entrypoint."""
import typer

from roboquote.entities.generation_options import GenerationOptions
from roboquote.picture import generate_picture, get_random_background_category
from roboquote.quote import get_random_quote

app = typer.Typer()


@app.command()
def generate(
    filename: str,
    blur: bool = typer.Option(False, help="Add a blur on the background."),
    blur_intensity: int = typer.Option(
        5, help="If blur is enabled,the blur intensity level."
    ),
) -> None:
    """Generate a new picture with the given filename."""
    # Get a random background category
    background_category = get_random_background_category()

    # Get text to use
    text = get_random_quote(background_category)
    generate_picture(
        GenerationOptions(
            text=text,
            filename=filename,
            background_category=background_category,
            blur=blur,
            blur_intensity=blur_intensity,
        )
    )


if __name__ == "__main__":
    app()
