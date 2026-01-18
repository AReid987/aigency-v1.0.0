"""
Logging configuration for the application
"""
import logging
import sys
from typing import Any, Dict
from app.core.config import settings

def setup_logging() -> None:
    """Configure application logging"""
    
    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Get log level from settings
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Configure root logger
    logging.basicConfig(
        level=log_level,
        handlers=[console_handler],
        force=True
    )
    
    # Set specific loggers
    loggers_config = {
        "uvicorn": logging.INFO,
        "uvicorn.access": logging.INFO,
        "sqlalchemy.engine": logging.WARNING,
        "celery": logging.INFO,
        "httpx": logging.WARNING,
    }
    
    for logger_name, level in loggers_config.items():
        logging.getLogger(logger_name).setLevel(level)

def get_logger(name: str) -> logging.Logger:
    """Get a logger with the given name"""
    return logging.getLogger(name)