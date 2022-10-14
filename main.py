"""Main CLI entrypoint."""
import typer

from inspirational_quotes_generator.picture import (
    generate_picture,
    get_random_background_category,
)
from inspirational_quotes_generator.quote import get_random_quote

app = typer.Typer()


@app.command()
def generate(filename: str) -> None:
    """Generate a new picture with the given filename."""
    # Get a random background category
    background_category = get_random_background_category()

    # Get text to use
    text = get_random_quote(background_category)
    generate_picture(text, filename, background_category)


if __name__ == "__main__":
    app()
