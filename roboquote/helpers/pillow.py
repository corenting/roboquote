"""Handle the multiline text wrapping for Pillow operations.

From https://github.com/atomicparade/pil_autowrap/blob/main/pil_autowrap/pil_autowrap.py by atomicparade (https://github.com/atomicparade) for the text wrapping
From https://stackoverflow.com/a/61730849 for the dominant color function
"""
import os
import random
from typing import Optional, Tuple

from loguru import logger
from PIL import Image
from PIL.ImageFont import FreeTypeFont, truetype

from roboquote import constants


def get_font_for_picture(picture_width: int) -> FreeTypeFont:
    """Get the font with correct size to use for the picture."""
    fonts = [
        file for file in os.listdir(f"{constants.FONTS_PATH}/") if file.endswith(".ttf")
    ]

    font_filename = random.choice(fonts)
    logger.debug(f"Using {font_filename} for font")

    font_size = picture_width // 20
    font_path = f"{constants.FONTS_PATH}/{font_filename}"
    return truetype(font_path, font_size)


def get_dominant_color(image: Image) -> tuple[int, int, int, int]:
    """Get the dominant color of an image as a tuple."""
    img = image.copy()
    img = img.convert("RGBA")
    img = img.resize((1, 1), resample=0)
    return img.getpixel((0, 0))


def wrap_text(
    font: FreeTypeFont,
    text: str,
    max_width: int,
    direction: str = "ltr",
) -> str:
    """Given a text, wraps it at the given width.

    :param font: Font to use.

    :param text: Text to fit.

    :param max_width: Maximum width of the final text, in pixels.

    :param max_height: Maximum height height of the final text, in pixels.

    :param spacing: The number of pixels between lines.

    :param direction: Direction of the text. It can be 'rtl' (right to
                      left), 'ltr' (left to right) or 'ttb' (top to bottom).
                      Requires libraqm.

    :return: The wrapped text.
    """
    words = text.split()

    lines: list[str] = [""]
    curr_line_width = 0

    for word in words:
        if curr_line_width == 0:
            word_width = font.getlength(word, direction)

            lines[-1] = word
            curr_line_width = word_width
        else:
            new_line_width = font.getlength(f"{lines[-1]} {word}", direction)

            if new_line_width > max_width:
                # Word is too long to fit on the current line
                word_width = font.getlength(word, direction)

                # Put the word on the next line
                lines.append(word)
                curr_line_width = word_width
            else:
                # Put the word on the current line
                lines[-1] = f"{lines[-1]} {word}"
                curr_line_width = new_line_width

    return "\n".join(lines)


def try_fit_text(
    font: FreeTypeFont,
    text: str,
    max_width: int,
    max_height: int,
    spacing: int = 4,
    direction: str = "ltr",
) -> Optional[str]:
    """Try to to wrap the text into a rectangle.

    Tries to fit the text into a box using the given font at decreasing sizes,
    based on ``scale_factor``. Makes ``max_iterations`` attempts.

    :param font: Font to use.

    :param text: Text to fit.

    :param max_width: Maximum width of the final text, in pixels.

    :param max_height: Maximum height height of the final text, in pixels.

    :param spacing: The number of pixels between lines.

    :param direction: Direction of the text. It can be 'rtl' (right to
                      left), 'ltr' (left to right) or 'ttb' (top to bottom).
                      Requires libraqm.

    :return: If able to fit the text, the wrapped text. Otherwise, ``None``.
    """
    words = text.split()

    line_height = font.size

    if line_height > max_height:
        # The line height is already too big
        return None

    lines: list[str] = [""]
    curr_line_width = 0

    for word in words:
        if curr_line_width == 0:
            word_width = font.getlength(word, direction)

            if word_width > max_width:
                # Word is longer than max_width
                return None

            lines[-1] = word
            curr_line_width = word_width
        else:
            new_line_width = font.getlength(f"{lines[-1]} {word}", direction)

            if new_line_width > max_width:
                # Word is too long to fit on the current line
                word_width = font.getlength(word, direction)
                new_num_lines = len(lines) + 1
                new_text_height = (new_num_lines * line_height) + (
                    new_num_lines * spacing
                )

                if word_width > max_width or new_text_height > max_height:
                    # Word is longer than max_width, and
                    # adding a new line would make the text too tall
                    return None

                # Put the word on the next line
                lines.append(word)
                curr_line_width = word_width
            else:
                # Put the word on the current line
                lines[-1] = f"{lines[-1]} {word}"
                curr_line_width = new_line_width

    return "\n".join(lines)


def fit_text(
    font: FreeTypeFont,
    text: str,
    max_width: int,
    max_height: int,
    spacing: int = 4,
    scale_factor: float = 0.8,
    max_iterations: int = 5,
    direction: str = "ltr",
) -> Tuple[FreeTypeFont, str]:
    """Automatically determines text wrapping and appropriate font size.

    Tries to fit the text into a box using the given font at decreasing sizes,
    based on ``scale_factor``. Makes ``max_iterations`` attempts.

    If unable to find an appropriate font size within ``max_iterations``
    attempts, wraps the text at the last attempted size.

    :param font: Font to use.

    :param text: Text to fit.

    :param max_width: Maximum width of the final text, in pixels.

    :param max_height: Maximum height height of the final text, in pixels.

    :param spacing: The number of pixels between lines.

    :param scale_factor:

    :param max_iterations: Maximum number of attempts to try to fit the text.

    :param direction: Direction of the text. It can be 'rtl' (right to
                      left), 'ltr' (left to right) or 'ttb' (top to bottom).
                      Requires libraqm.

    :return: The font at the appropriate size and the wrapped text.
    """
    initial_font_size = font.size

    for i in range(max_iterations):
        trial_font_size = int(initial_font_size * pow(scale_factor, i))
        trial_font = font.font_variant(size=trial_font_size)

        wrapped_text = try_fit_text(
            trial_font,
            text,
            max_width,
            max_height,
            spacing,
            direction,
        )

        if wrapped_text:
            return (trial_font, wrapped_text)

    # Give up and wrap the text at the last size
    wrapped_text = wrap_text(trial_font, text, max_width, direction)

    return (trial_font, wrapped_text)
