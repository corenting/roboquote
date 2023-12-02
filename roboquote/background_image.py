"""Functions to get a background for the result image."""
import random
from io import BytesIO

import httpx
from PIL import Image

from roboquote.entities.exceptions import CannotFetchBackgroundError
from roboquote.entities.image_credits import ImageCredits


def get_random_background_search_query() -> str:
    """Get a random background theme."""
    return random.choice(
        [
            "sea",
            "sunrise",
            "mountain",
            "sand beach",
            "desert",
            "forest",
            "calm landscape",
        ]
    )


def get_random_background_from_unsplash_by_theme(
    background_search_query: str,
) -> tuple[Image, ImageCredits]:
    """Get a random background given a search query."""
    response = httpx.get(
        "https://unsplash.com/napi/search/photos?query="
        + background_search_query
        + " background&orientation=landscape"
    )

    if not response.is_success:
        raise CannotFetchBackgroundError()

    content = response.json()["results"]
    items = [item for item in content if not item["premium"]]

    random_background = random.choice(items)
    picture_url = random_background["urls"]["full"]

    image_response = httpx.get(picture_url)
    image = Image.open(BytesIO(image_response.content))
    credits = ImageCredits(
        username=random_background["user"]["username"],
        first_name=random_background["user"]["first_name"],
        last_name=random_background["user"]["last_name"],
        url=random_background["links"]["html"],
    )

    return image, credits
