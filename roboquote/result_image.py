"""Handle the image-related tasks."""

from loguru import logger
from PIL import Image, ImageDraw, ImageFilter

from roboquote.entities.generate_options import GenerateOptions
from roboquote.helpers.pillow import fit_text, get_dominant_color, get_font_for_image


def generate_image(options: GenerateOptions) -> Image.Image:
    """Generate and return an image
    with the given filename for a given text and category.
    """
    image = options.background_image.copy()
    width = image.width
    height = image.height

    if options.blur:
        blur_intensity = (
            options.blur_intensity if options.blur_intensity is not None else 5
        )
        image = image.filter(ImageFilter.GaussianBlur(blur_intensity))

    draw = ImageDraw.Draw(image)

    font = get_font_for_image(width)
    font, fitted_text = fit_text(
        font, options.text, int(width / 1.2), int(height / 1.2)
    )

    # Compute position for text
    common_args = {
        "xy": (width / 2, height / 2),
        "text": fitted_text,
        "anchor": "mm",
        "align": "center",
        "font": font,
    }

    # Get bounding box of text
    text_bounding_box = draw.multiline_textbbox(**common_args)

    # For the bounding box of the text, get dominant color to compute text color
    dominant_bg_r, dominant_bg_g, dominant_bg_b, _ = get_dominant_color(
        image, text_bounding_box
    )
    luma = dominant_bg_r * 0.299 + dominant_bg_g * 0.587 + dominant_bg_b * 0.114
    logger.debug(f"Background luma: {luma}")
    text_color = "#000000" if luma > 170 else "#FFFFFF"

    # Draw the text
    draw.multiline_text(
        fill=text_color,
        stroke_fill="#000000" if text_color == "#FFFFFF" else "#FFFFFF",
        stroke_width=4,
        **common_args,
    )

    return image
