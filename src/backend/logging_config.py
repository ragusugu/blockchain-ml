"""
Centralized Logging Configuration
Call setup_logging() once at application startup.
"""
import logging
import os


def setup_logging(level: str = None):
    """
    Configure logging once for the entire application.

    Args:
        level: Logging level string (DEBUG, INFO, WARNING, ERROR).
               Defaults to LOG_LEVEL env var or INFO.
    """
    log_level = level or os.getenv('LOG_LEVEL', 'INFO')

    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        force=True  # Override any previous basicConfig calls
    )

    # Suppress noisy third-party loggers
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('web3').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
