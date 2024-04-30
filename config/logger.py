import logging
import os


def setup_logging():
    format = "[%(asctime)s] %(levelname)s | %(name)s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(level=logging.INFO, format=format, datefmt=datefmt)
    logging.getLogger().setLevel(logging.INFO)
    if os.environ.get("DEBUG", "False").lower() in ("true", "1"):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.WARNING)
        logging.getLogger("requests").setLevel(logging.WARNING)
        logging.getLogger("bs4").setLevel(logging.WARNING)
