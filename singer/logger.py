import logging
import logging.config


def get_logger(name='singer'):
    """Return a Logger instance to use in singer."""
    return logging.getLogger(name)
