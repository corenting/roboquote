from dataclasses import dataclass
from enum import Enum


class LargeLanguageModelPromptType(Enum):
    CONTINUE = "continue"  # where the model continues an existing sentence
    CHAT = "chat"  # where we chat with the model


class LargeLanguageModelAPI(Enum):
    GROQ_CLOUD = "GroqCloud"
    HUGGING_FACE = "Hugging Face"


@dataclass
class LargeLanguageModel:
    name: str
    prompt_type: LargeLanguageModelPromptType
    api: LargeLanguageModelAPI
    prompt_start: str | None = None
    prompt_end: str | None = None
