"""Functions to get a background for the result image."""

import random
import ssl
from io import BytesIO

import certifi
import httpx
from loguru import logger
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


async def get_random_background_from_unsplash_by_theme(
    background_search_query: str,
) -> tuple[Image.Image, ImageCredits]:
    """Get a random background given a search query."""

    # The default httpx verify context doesn't work with
    # unsplash, it results in 403 errors
    context = ssl.create_default_context()
    context.load_verify_locations(certifi.where())

    async with httpx.AsyncClient(verify=context) as client:
        url = (
            "https://unsplash.com/napi/search/photos?orientation=landscape&page=1"
            "&per_page=20&plus=none&query={background_search_query} background"
            "&xp=search-disable-curation:experiment"
        )
        response = await client.get(url)

    if not response.is_success:
        logger.debug(
            f"Error {response.status_code} from Unsplash API",
        )
        raise CannotFetchBackgroundError()

    content = response.json()["results"]
    items = [item for item in content if not item["premium"]]

    random_background = random.choice(items)
    picture_url = random_background["urls"]["full"]

    async with httpx.AsyncClient() as client:
        image_response = await client.get(picture_url)
    image = Image.open(BytesIO(image_response.content))
    credits = ImageCredits(
        username=random_background["user"]["username"],
        first_name=random_background["user"]["first_name"],
        last_name=random_background["user"]["last_name"],
        url=random_background["links"]["html"],
    )

    return image, credits
