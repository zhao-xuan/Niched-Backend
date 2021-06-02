import logging
import sys

from niched.core.config import LOGGING_LEVEL

logger = logging.getLogger(__name__)

log_format = '[%(levelname)s] %(asctime)s - %(name)s : %(message)s'
logging.basicConfig(format=log_format, level=LOGGING_LEVEL)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(LOGGING_LEVEL)
logger.addHandler(handler)
