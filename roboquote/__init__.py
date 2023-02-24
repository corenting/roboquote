import sys
import nltk


from loguru import logger

from roboquote import config

# Setup logger
logger.remove()
logger.add(sys.stderr, level=config.LOG_LEVEL)

# Download nltk data for quote text generation
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")
    logger.error("Missing data downloaded, please relaunch roboquote.")
