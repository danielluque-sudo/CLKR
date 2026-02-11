# utils/logger.py
import logging
import os
from datetime import datetime
import config


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with file and console handlers

    Args:
        name: Logger name
        level: Logging level

    Returns:
        Configured logger
    """
    # Create logs directory if it doesn't exist
    os.makedirs(config.LOGS_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )

    # File handler - detailed logs
    log_file = os.path.join(
        config.LOGS_DIR,
        f'{name}_{datetime.now().strftime("%Y%m%d")}.log'
    )
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)

    # Console handler - simpler logs
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def log_scraper_stats(logger: logging.Logger, stats: dict):
    """
    Log scraper statistics in a formatted way

    Args:
        logger: Logger instance
        stats: Dictionary of statistics
    """
    logger.info("=" * 50)
    logger.info("SCRAPER STATISTICS")
    logger.info("=" * 50)

    for key, value in stats.items():
        logger.info(f"{key}: {value}")

    logger.info("=" * 50)
