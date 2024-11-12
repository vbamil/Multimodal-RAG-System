# backend/app/src/utils/logger.py

import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str) -> logging.Logger:
    """
    Set up and configure a logger.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent adding multiple handlers if the logger already has them
    if not logger.handlers:
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create rotating file handler
        log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', '..', 'logs')
        os.makedirs(log_dir, exist_ok=True)
        file_handler = RotatingFileHandler(os.path.join(log_dir, 'app.log'), maxBytes=5*1024*1024, backupCount=5)
        file_handler.setLevel(logging.INFO)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
