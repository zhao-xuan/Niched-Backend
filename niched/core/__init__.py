import logging
import sys

from niched.core.config import LOGGING_LEVEL

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(LOGGING_LEVEL)
formatter = logging.Formatter('[%(levelname)s] - %(asctime)s - %(name)s : %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
