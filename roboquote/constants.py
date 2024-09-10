"""Constants used in the code."""

from roboquote.entities.large_language_model import (
    LargeLanguageModel,
    LargeLanguageModelAPI,
    LargeLanguageModelPromptType,
)

FONTS_PATH = "fonts"

# Ordered by preferred models
AVAILABLE_LARGE_LANGUAGE_MODELS = [
    LargeLanguageModel(
        name="llama3-70b-8192",
        prompt_type=LargeLanguageModelPromptType.CHAT,
        api=LargeLanguageModelAPI.GROQ_CLOUD,
    ),
    LargeLanguageModel(
        name="mistralai/Mixtral-8x7B-Instruct-v0.1",
        prompt_type=LargeLanguageModelPromptType.CHAT,
        api=LargeLanguageModelAPI.HUGGING_FACE,
        prompt_start="<s>[INST]",
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

DEFAULT_LARGE_LANGUAGE_MODEL = AVAILABLE_LARGE_LANGUAGE_MODELS[0]
