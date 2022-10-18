"""Handle the picture-related tasks."""
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from roboquote import constants
from roboquote.entities.generation_options import GenerationOptions
from roboquote.helpers.pillow import fit_text, get_dominant_color

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


def generate_picture(options: GenerationOptions) -> None:
    """Generate and save a picture with the given filename for a given text and category."""
    with Image.open(
        f"{constants.PICTURES_PATH}/{options.background_category}/{get_random_background_filename_by_category(options.background_category)}"
    ) as image:
        width = image.width
        height = image.height

        # Get dominant background color
        dominant_bg_r, dominant_bg_g, dominant_bg_b, dominant_bg_a = get_dominant_color(
            image
        )
        if (
            dominant_bg_r * 0.299
            + dominant_bg_g * 0.587
            + dominant_bg_b * 0.114
            + (1 - dominant_bg_a) * 255
        ) > 186:
            text_color = "#000000"
        else:
            text_color = "#FFFFFF"

        if options.blur:
            image = image.filter(ImageFilter.GaussianBlur(5))

        draw = ImageDraw.Draw(image)

        font = _get_font_for_picture(width)
        font, fitted_text = fit_text(font, options.text, width - 200, height - 200)

        draw.multiline_text(
            (width / 2, height / 2),
            fitted_text,
            anchor="mm",
            align="center",
            font=font,
            fill=text_color,
        )

        image.save(options.filename)
