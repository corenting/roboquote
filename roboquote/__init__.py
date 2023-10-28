import sys

from loguru import logger

from roboquote import config

# Setup logger
logger.remove()
logger.add(sys.stderr, level=config.LOG_LEVEL)
