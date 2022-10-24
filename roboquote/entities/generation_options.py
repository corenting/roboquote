"""Entity to represent the generation options."""
from dataclasses import dataclass

from PIL import Image


@dataclass
class GenerationOptions:
    """The options when generating a picture."""

    text: str
    output_filename: str
    background_image: Image

    blur: bool
    blur_intensity: int
