import logging
import os


def log_level():
    levels = {
        "FATAL": logging.FATAL,
        "CRITICAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }
    return levels.get(os.getenv("LOG_LEVEL", "ERROR").upper())


__LOG_LEVEL__ = log_level()


def init_logger(name: str = None, level=__LOG_LEVEL__):
    logging.basicConfig(
        format=("%(asctime)s [%(levelname)7s] %(name)-16s %(message)s"),
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logger = logging.getLogger(name) if name else logging.getLogger()
    logger.setLevel(level=level)
    return logger
