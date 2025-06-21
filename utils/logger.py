import datetime
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

FORMATTER = logging.Formatter("%(asctime)s — %(name)s — %(levelname)s — %(message)s")

# Get the current directory where the script is located
current_directory = Path(__file__).parent

# Create the log directory at the same level as the "engines" directory
log_directory = current_directory / "../log"
log_directory.mkdir(parents=True, exist_ok=True)

# Use the current date to construct the log file name
LOG_FILE = log_directory / f"{str(datetime.date.today())}.log"
ERROR_LOG_FILE = log_directory / f"{str(datetime.date.today())}.log.error"


def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(log_file):
    file_handler = TimedRotatingFileHandler(log_file, when='midnight')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(logger_name="default_logger", log_dir=None):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)  # better to have too much log than not enough
    logger.addHandler(get_console_handler())

    if log_dir is None:
        # Use default LOG_FILE
        logger.addHandler(get_file_handler(LOG_FILE))
    else:
        # Use the provided log_dir with the current date as part of the file name
        log_file = log_directory / f"{log_dir}"
        logger.addHandler(get_file_handler(log_file))

    # with this pattern, it's rarely necessary to propagate the error up to parent
    logger.propagate = False
    return logger


# class Logger:
#     _instance = None
#     _logger = None
#
#     def __new__(cls, *args, **kwargs):
#         if not cls._instance:
#             cls._instance = super(Logger, cls).__new__(cls, *args, **kwargs)
#             cls._instance._logger = get_logger()
#         return cls._instance
#
#     @property
#     def logger(self):
#         return self._logger
