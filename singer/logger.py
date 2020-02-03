import logging
import logging.config
import os


def get_logger(name='singer'):
    """Return a Logger instance to use in singer."""
    if 'LOGGING_CONF_FILE' in os.environ and os.environ['LOGGING_CONF_FILE']:
        path = os.environ['LOGGING_CONF_FILE']
        logging.config.fileConfig(path, disable_existing_loggers=False)

    return logging.getLogger(name)
