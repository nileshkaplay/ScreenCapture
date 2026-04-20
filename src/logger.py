"""Application logging configuration."""
import logging
from logging.handlers import RotatingFileHandler
from config import LOG_FILE

# Ensure the log file directory exists
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("screenshot_capture")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    handler = RotatingFileHandler(LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
