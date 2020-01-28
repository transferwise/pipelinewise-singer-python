import logging
import logging.config


def get_logger():
    """Return a Logger instance to use in singer."""
    return logging.getLogger('singer')
