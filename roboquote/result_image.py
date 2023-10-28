"""Handle the image-related tasks."""

from loguru import logger
from PIL import Image, ImageDraw, ImageFilter

from roboquote.entities.generate_options import GenerateOptions
from roboquote.helpers.pillow import fit_text, get_dominant_color, get_font_for_image


def generate_image(options: GenerateOptions) -> Image:
    """Generate and return an image
    with the given filename for a given text and category.
    """
    image = options.background_image.copy()
    width = image.width
    height = image.height

    # Get dominant background color
    dominant_bg_r, dominant_bg_g, dominant_bg_b, _ = get_dominant_color(image)
    luma = dominant_bg_r * 0.299 + dominant_bg_g * 0.587 + dominant_bg_b * 0.114
    logger.debug(f"Background luma: {luma}")
    text_color = "#000000" if luma > 200 else "#FFFFFF"

    if options.blur:
        blur_intensity = (
            options.blur_intensity if options.blur_intensity is not None else 5
        )
        image = image.filter(ImageFilter.GaussianBlur(blur_intensity))

    draw = ImageDraw.Draw(image)

    font = get_font_for_image(width)
    font, fitted_text = fit_text(font, options.text, width - 200, height - 200)

    draw.multiline_text(
        (width / 2, height / 2),
        fitted_text,
        anchor="mm",
        align="center",
        font=font,
        fill=text_color,
        stroke_width=2,
        stroke_fill="#000000" if text_color == "#FFFFFF" else "#FFFFFF",
    )

    return image
