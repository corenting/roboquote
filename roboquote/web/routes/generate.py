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
from roboquote.entities.text_model import TextModel
from roboquote.quote_text_generation import get_random_quote
from roboquote.result_image import generate_image


async def generate(request: Request) -> Response:
    """For a given request, generate the corresponding quote image."""

    # Get request parameters
    if len(request.query_params.get("background", "")) > 0:
        background = str(request.query_params["background"])
    else:
        background = get_random_background_search_query()
    text_model = TextModel(str(request.query_params["text_model"]))
    blur: bool = True if request.query_params.get("blur", "on") == "on" else False

    # Get background image
    (
        background_image,
        background_image_credits,
    ) = await get_random_background_from_unsplash_by_theme(background)

    # Get text to use
    text = await get_random_quote(background, text_model)

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
        headers={
            "X-Image-Credits": json.dumps(asdict(background_image_credits)),
            "X-Generation-Parameters": json.dumps(
                {
                    "background": background,
                    "blur": blur,
                    "text_model": text_model.value,
                }
            ),
        },
    )


routes = [
    Route("/", endpoint=generate),
]
