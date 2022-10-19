"""Handle the picture-related tasks."""

from PIL import Image, ImageDraw, ImageFilter

from roboquote import constants
from roboquote.background_picture import get_random_background_filename_by_theme
from roboquote.entities.generation_options import GenerationOptions
from roboquote.helpers.pillow import fit_text, get_dominant_color, get_font_for_picture


def generate_picture(options: GenerationOptions) -> None:
    """Generate and save a picture with the given filename for a given text and category."""
    with Image.open(
        f"{constants.PICTURES_PATH}/{options.background_theme.value}/{get_random_background_filename_by_theme(options.background_theme)}"
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

        font = get_font_for_picture(width)
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
