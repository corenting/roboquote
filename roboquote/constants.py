"""Constants used in the code."""

from roboquote.entities.large_language_model import (
    LargeLanguageModel,
    LargeLanguageModelAPI,
)

FONTS_PATH = "fonts"

# Ordered by preferred models
AVAILABLE_LARGE_LANGUAGE_MODELS = [
    LargeLanguageModel(
        name="llama-3.3-70b-versatile",
        api=LargeLanguageModelAPI.GROQ_CLOUD,
    ),
    LargeLanguageModel(
        name="deepseek-r1-distill-llama-70b",
        api=LargeLanguageModelAPI.GROQ_CLOUD,
    ),
    LargeLanguageModel(
        name="mixtral-8x7b-32768",
        api=LargeLanguageModelAPI.GROQ_CLOUD,
    ),
]

AVAILABLE_LARGE_LANGUAGE_MODELS_NAMES = [
    model.name for model in AVAILABLE_LARGE_LANGUAGE_MODELS
]

DEFAULT_LARGE_LANGUAGE_MODEL = AVAILABLE_LARGE_LANGUAGE_MODELS[0]
