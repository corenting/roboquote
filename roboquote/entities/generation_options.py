"""Entity to represent the generation options."""
from dataclasses import dataclass


@dataclass
class GenerationOptions:
    """The options when generating a picture."""

    text: str
    filename: str
    background_category: str

    blur: bool
    blur_intensity: int
