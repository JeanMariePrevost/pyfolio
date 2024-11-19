import datetime
import logging
import os

from colorama import Back

try:
    from colorama import Fore, Style, init

    COLORAMA_AVAILABLE = True
    init(autoreset=True)  # Automatically reset colors after each log line
except ImportError:
    COLORAMA_AVAILABLE = False

import path_util

__logger = None

LOG_TO_FILE = True
LOG_TO_CONSOLE = True
LOG_LEVEL = logging.DEBUG


class ColoredFormatter(logging.Formatter):
    """Custom formatter to add colors to the entire log string."""

    LEVEL_COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Back.RED + Fore.WHITE,
        logging.CRITICAL: Back.RED + Fore.WHITE + Style.BRIGHT,
    }

    def format(self, record):
        # Apply color to the entire log string
        log_color = self.LEVEL_COLORS.get(record.levelno, "")
        reset_color = Style.RESET_ALL if COLORAMA_AVAILABLE else ""
        log_line = super().format(record)
        return f"{log_color}{log_line}{reset_color}"


def get_logger():
    """Returns the custom logger instance."""
    global __logger
    if __logger is None:
        setup_logger()
    return __logger


def setup_logger():
    """Sets up the custom logger and attaches handlers."""
    global __logger
    if __logger is not None:
        return  # Prevent re-initializing the logger

    # Create a custom logger
    __logger = logging.getLogger("pyfolio")
    __logger.setLevel(LOG_LEVEL)
    __logger.propagate = False  # Ensure logs do not propagate to the root logger

    # Create handlers
    handlers = []

    if LOG_TO_FILE:
        log_file = path_util.resolve_path("logs") + "/" + datetime.datetime.now().strftime("%Y-%m-%d") + ".log"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)  # Ensure the directory exists
        open(log_file, "a").close()  # Ensure the file exists

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        handlers.append(file_handler)

    if LOG_TO_CONSOLE:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColoredFormatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        handlers.append(console_handler)

    # Add handlers to the custom logger
    for handler in handlers:
        __logger.addHandler(handler)


def __log(level, message):
    """Helper function to log a message at a specific level."""
    get_logger().log(level, message)


def debug(message):
    """Logs a debug message."""
    __log(logging.DEBUG, message)


def info(message):
    """Logs an info message."""
    __log(logging.INFO, message)


def warning(message):
    """Logs a warning message."""
    __log(logging.WARNING, message)


def error(message):
    """Logs an error message."""
    __log(logging.ERROR, message)


def critical(message):
    """Logs a critical message."""
    __log(logging.CRITICAL, message)
