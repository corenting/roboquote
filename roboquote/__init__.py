import sys

from loguru import logger

from roboquote import config

__version__ = "0.5.0"

# Setup logger
logger.remove()
logger.add(sys.stderr, level=config.LOG_LEVEL)
