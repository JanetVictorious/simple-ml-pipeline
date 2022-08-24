import os
import sys
from typing import Optional
import logging
from datetime import datetime


def get_logger(log_path: str,
               name_suffix: Optional[str] = None,
               logging_level: Optional[str] = 'INFO') -> logging.Logger:
    """
    Construct logger and store.

    :param str logger_path:
        Path for logger output.
    :param str name_suffix:
        Suffix for logger file.
    :return:
        Logger object.
    :rtype:
        logger.Logger
    """
    if not os.path.exists(log_path):
        os.makedirs(name=log_path, exist_ok=True)

    # Create timestamp and name for logger
    now_str = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}"
    logger_fname = f'{log_path}/{now_str}'

    # Append suffix if provided and .log
    logger_fname += f'_{name_suffix}.log' if name_suffix else '.log'

    # Create formatter
    log_format = '%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s'  # noqa: E501
    stream_formatter = logging.Formatter(log_format)

    # Create file formatter
    date_format = '%Y-%m-%d %H:%M:%S'
    file_formatter = logging.Formatter(log_format, datefmt=date_format)

    # Create logger
    logger = logging.getLogger(__name__)

    # Set logging level
    if logging_level == 'DEBUG':
        level = logging.DEBUG
    elif logging_level == 'WARNING':
        level = logging.WARNING
    elif logging_level == 'ERROR':
        level = logging.ERROR
    elif logging_level == 'CRITICAL':
        level = logging.CRITICAL
    else:
        level = logging.INFO
    logger.setLevel(level)

    # Fix for erroneous logger duplication
    logger.handlers = []

    # Create file handler
    file_handler = logging.FileHandler(filename=logger_fname)
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(stream_formatter)
    logger.addHandler(console_handler)

    return logger
