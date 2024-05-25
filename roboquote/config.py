"""Handle the configuration loaded from the environment."""

from environs import Env

env = Env()
env.read_env()

WEB_DEBUG: bool = env.bool("WEB_DEBUG", False)
LOG_LEVEL: str = env.str("LOG_LEVEL", "WARNING")

HUGGING_FACE_ACCESS_TOKEN: str = env.str("HUGGING_FACE_ACCESS_TOKEN")
GROQ_CLOUD_API_KEY: str = env.str("GROQ_CLOUD_API_KEY")
