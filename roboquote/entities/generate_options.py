"""Entity to represent the generation options."""
from dataclasses import dataclass
from typing import Optional

from PIL import Image


@dataclass
class GenerateOptions:
    """The options when generating a image."""

    text: str
    background_image: Image

    blur: bool
    blur_intensity: Optional[int]
