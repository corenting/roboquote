"""Entity to represent the generation options."""
from dataclasses import dataclass

from roboquote.entities.themes import Theme


@dataclass
class GenerationOptions:
    """The options when generating a picture."""

    text: str
    filename: str
    background_theme: Theme

    blur: bool
    blur_intensity: int
