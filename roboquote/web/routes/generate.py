"""Handle the route for image generation."""
import json
from dataclasses import asdict
from io import BytesIO

from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route

from roboquote.background_image import (
    get_random_background_from_unsplash_by_theme,
    get_random_background_search_query,
)
from roboquote.entities.generate_options import GenerateOptions
from roboquote.quote_text_generation import get_random_quote
from roboquote.result_image import generate_image


async def generate(request: Request) -> Response:
    """For a given request, generate the corresponding quote image."""
    # Get input parameters
    if "background" in request.query_params:
        background = str(request.query_params["background"])
    else:
        background = get_random_background_search_query()
    blur: bool = True

    # Get background image
    (
        background_image,
        background_image_credits,
    ) = get_random_background_from_unsplash_by_theme(background)

    # Get text to use
    text = get_random_quote(background)

    # Generate image
    generate_options = GenerateOptions(
        background_image=background_image,
        blur=blur,
        blur_intensity=None,
        text=text,
    )
    image = generate_image(generate_options)
    image_as_bytes = BytesIO()
    image.save(image_as_bytes, format="JPEG")

    return Response(
        image_as_bytes.getvalue(),
        media_type="image/jpeg",
        headers={"X-Image-Credits": json.dumps(asdict(background_image_credits))},
    )


routes = [
    Route("/", endpoint=generate),
]
