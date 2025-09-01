import logging
import sys
from typing import Optional

project_name = 'Generator'
logger = logging.getLogger(project_name)

def configure_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_to_console: bool = True,
    log_format: str = "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
) -> None:
    """
    Configure the logger for the project.
    
    Args:
        log_level (str): Logging level (e.g., 'INFO', 'DEBUG').
        log_file (Optional[str]): Path to the log file. If None, file logging is disabled.
        log_to_console (bool): Whether to log to the console (stdout).
        log_format (str): Format string for log messages.
    """
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    logger.propagate = False

    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    for name in logging.root.manager.loggerDict:
        if name != project_name:
            logging.getLogger(name).setLevel(logging.CRITICAL + 1)

    formatter = logging.Formatter(log_format)

    if not logger.handlers:
        if log_to_console:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        if log_file:
            try:
                file_handler = logging.FileHandler(log_file)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            except Exception as e:
                sys.stderr.write(f"Error setting up file logger to {log_file}: {e}\\n")
                if not log_to_console:
                    sys.exit(1)