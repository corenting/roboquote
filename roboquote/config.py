"""Handle the configuration loaded from the environment."""

from environs import Env

env = Env()
env.read_env()

WEB_DEBUG: bool = env.bool("WEB_DEBUG", False)
HUGGING_FACE_API_TOKEN: str = env.str("HUGGING_FACE_API_TOKEN")
LOG_LEVEL: str = env.str("LOG_LEVEL", "WARNING")
