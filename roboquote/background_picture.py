"""Functions to get a background for the result picture."""
import os
import random

from roboquote import constants

backgrounds_categories: list[str] = [
    name
    for name in os.listdir(constants.PICTURES_PATH)
    if os.path.isdir(os.path.join(constants.PICTURES_PATH, name))
]


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
