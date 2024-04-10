from enum import Enum


class TextModel(Enum):
    BLOOM = "bigscience/bloom"
    MISTRAL_8X7B_INSTRUCT = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    COHERE_COMMAND_R_PLUS = "CohereForAI/c4ai-command-r-plus"
