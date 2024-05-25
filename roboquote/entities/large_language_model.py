from dataclasses import dataclass
from enum import Enum


class LargeLanguageModelPromptType(Enum):
    CONTINUE = "continue"  # where the model continues an existing sentence
    INSTRUCT = "instruct"  # where we instruct the model


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


# Ordered by preferred models
AVAILABLE_LARGE_LANGUAGE_MODELS = [
    LargeLanguageModel(
        name="llama3-70b-8192",
        prompt_type=LargeLanguageModelPromptType.INSTRUCT,
        api=LargeLanguageModelAPI.GROQ_CLOUD,
    ),
    LargeLanguageModel(
        name="mistralai/Mixtral-8x7B-Instruct-v0.1",
        prompt_type=LargeLanguageModelPromptType.INSTRUCT,
        api=LargeLanguageModelAPI.HUGGING_FACE,
        prompt_start="<s>[[INST]",
        prompt_end="[/INST]",
    ),
    LargeLanguageModel(
        name="bigscience/bloom",
        prompt_type=LargeLanguageModelPromptType.CONTINUE,
        api=LargeLanguageModelAPI.HUGGING_FACE,
    ),
]

AVAILABLE_LARGE_LANGUAGE_MODELS_NAMES = [
    model.name for model in AVAILABLE_LARGE_LANGUAGE_MODELS
]
