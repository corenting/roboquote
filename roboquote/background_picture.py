"""Functions to get a background for the result picture."""
import random

import requests
from PIL import Image

from roboquote.entities.exceptions import CannotFetchBackgroundException


def get_random_background_search_query() -> str:
    """Get a random background theme."""
    return random.choice(["sea", "sunrise", "mountain", "sand beach"])


def get_random_background_from_unsplash_by_theme(background_search_query: str) -> Image:
    """Get a random background given a search query."""
    response = requests.get(
        f"https://unsplash.com/napi/search?query={background_search_query} background"
    )

    if not response.ok:
        raise CannotFetchBackgroundException("Error fetching background")

    content = response.json()["photos"]["results"]
    items = [
        item
        for item in content
        if not item["premium"] and item["width"] > item["height"]
    ]
    random_background = random.choice(items)

    return Image.open(requests.get(random_background["urls"]["full"], stream=True).raw)
