"""
Logging configuration for the Trading Bot.
Ensures all trading activity, API requests/responses, and errors are logged
to logs/trading.log with proper timestamp formatting.
"""

import os
import logging
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
LOG_FILE = os.path.join(LOG_DIR, "trading.log")

def setup_logger(name: str = "trading_bot") -> logging.Logger:
    """
    Sets up and returns a configured logger instance.
    Logs INFO and higher to logs/trading.log.
    Logs ERROR and higher to the console.
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    
    # Avoid adding handlers multiple times if logger is already configured
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        logger.propagate = False

        # Formatter: Timestamp - LoggerName - LogLevel - Message
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # File Handler (Rotating log file up to 5MB, keep 3 backups)
        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8"
        )
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Console Handler (Only for warnings and errors to keep CLI output clean)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
