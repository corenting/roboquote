from dataclasses import dataclass
from enum import Enum


class LargeLanguageModelAPI(Enum):
    GROQ_CLOUD = "GroqCloud"


@dataclass
class LargeLanguageModel:
    name: str
    api: LargeLanguageModelAPI
