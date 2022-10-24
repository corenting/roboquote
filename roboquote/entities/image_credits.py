"""Image credits dataclass."""

from dataclasses import dataclass


@dataclass
class ImageCredits:
    """Image credits dataclass."""

    username: str
    first_name: str
    last_name: str
    url: str
