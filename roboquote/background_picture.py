"""Functions to get a background for the result picture."""
import os
import random

from roboquote import constants
from roboquote.entities.themes import Theme


def get_random_background_theme() -> Theme:
    """Get a random background category."""
    return random.choice(list(Theme))


def get_random_background_filename_by_theme(background_theme: Theme) -> str:
    """Get a random background given a category."""
    backgrounds = [
        file
        for file in os.listdir(f"{constants.PICTURES_PATH}/{background_theme.value}/")
        if file.endswith(".jpg")
    ]

    return random.choice(backgrounds)
