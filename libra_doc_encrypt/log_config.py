import os
import logging
from datetime import datetime
import logging.config
from colorlog import ColoredFormatter

from .config import APP_NAME, LOG_FILENAME_FORMAT


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            '()': ColoredFormatter,
            'format': '%(log_color)s %(asctime)s - %(name)s - %(levelname)s - %(message)s%(reset)s',
        },
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        }
    },
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
            'level': 'INFO',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'filename': None,
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
            'mode': 'w',
            'encoding': 'utf-8',
        },
    },
    'root': {
        'handlers': ['stream', 'file'],
        'level': 'DEBUG',
    },
}


def configure_base_log(logger_handle: str = APP_NAME, log_dir: str = '.',
                       log_file: str = None, debug: bool = False) -> logging.Logger:
    if not log_file:
        log_file = LOG_FILENAME_FORMAT.format(datetime.now().strftime('%d-%m-%Y_%H-%M-%S'))
    log_config = dict(LOGGING)
    if log_dir != '.':
        os.makedirs(log_dir, exist_ok=True)
    log_config['handlers']['file']['filename'] = os.path.join(log_dir, log_file)


def get_child(child_handle: str, base_handle: str = APP_NAME) -> logging.Logger:
    pass


def get_logger(logger_handle: str) -> logging.Logger:
    pass
