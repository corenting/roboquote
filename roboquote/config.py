"""Handle the configuration loaded from the environment."""
from environs import Env

env = Env()
env.read_env()

DEBUG = env.bool("DEBUG", False)
HUGGING_FACE_API_TOKEN = env.str("HUGGING_FACE_API_TOKEN")
LOG_LEVEL = env.str("LOG_LEVEL", "ERROR")
