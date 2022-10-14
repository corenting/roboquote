"""Handle the picture-related tasks."""
import os
import random

from PIL import Image, ImageDraw, ImageFont

from inspirational_quotes_generator import constants
from inspirational_quotes_generator.helpers.pillow_text import fit_text

backgrounds_categories: list[str] = [
    name
    for name in os.listdir(constants.PICTURES_PATH)
    if os.path.isdir(os.path.join(constants.PICTURES_PATH, name))
]

fonts = list(os.listdir(constants.FONTS_PATH))


def _get_font_for_picture(picture_width: int) -> ImageFont.FreeTypeFont:
    """Get the font to use for the picture."""
    font_size = picture_width // 25
    font_path = f"{constants.FONTS_PATH}/Satisfy-Regular.ttf"
    return ImageFont.truetype(font_path, font_size)


def get_random_background_category() -> str:
    """Get a random background category."""
    return random.choice(backgrounds_categories)


def get_random_background_filename_by_category(background_category: str) -> str:
    """Get a random background given a category."""
    backgrounds = [
        file
        for file in os.listdir(f"{constants.PICTURES_PATH}/{background_category}/")
        if file.endswith(".jpg")
    ]

    return random.choice(backgrounds)


def generate_picture(text: str, filename: str, background_category: str) -> None:
    """Generate and save a picture with the given filename for a given text and category."""
    with Image.open(f"{constants.PICTURES_PATH}/{background_category}/1.jpg") as image:
        width = image.width
        height = image.height


        font = _get_font_for_picture(width)

        draw = ImageDraw.Draw(image)

        font, fitted_text = fit_text(font, text, width - 200, height - 200)

        draw.multiline_text(
            (width / 2, height / 2), fitted_text, anchor="mm", align="center", font=font
        )

        image.save(filename)
