"""Functions to get a background for the result picture."""
import random

import requests
from PIL import Image

from roboquote.entities.exceptions import CannotFetchBackgroundException
from roboquote.entities.image_credits import ImageCredits


def get_random_background_search_query() -> str:
    """Get a random background theme."""
    return random.choice(["sea", "sunrise", "mountain", "sand beach"])


def get_random_background_from_unsplash_by_theme(
    background_search_query: str,
) -> tuple[Image, ImageCredits]:
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
    picture_url = random_background["urls"]["full"]

    image = Image.open(requests.get(picture_url, stream=True).raw)
    credits = ImageCredits(
        username=random_background["user"]["username"],
        first_name=random_background["user"]["first_name"],
        last_name=random_background["user"]["last_name"],
        url=random_background["links"]["html"],
    )

    return image, credits
