
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    config_logging = {
        'level': logging.DEBUG,
        'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        'handlers': []
    }

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(config_logging['format']))
    config_logging['handlers'].append(console_handler)

    # File handler
    log_file = 'data/logs/application.log'
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter(config_logging['format']))
    config_logging['handlers'].append(file_handler)

    logging.basicConfig(**config_logging)
