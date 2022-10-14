"""Handle the configuration loaded from the environment."""
from environs import Env

env = Env()
env.read_env()

HUGGING_FACE_API_TOKEN = env.str("HUGGING_FACE_API_TOKEN")
