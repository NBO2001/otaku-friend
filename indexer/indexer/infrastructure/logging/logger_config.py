import logging
import sys
from pathlib import Path
from typing import Optional


class LoggerConfig:
    """Configuration and setup for application logging."""
    
    @staticmethod
    def setup_logger(
        name: str = "anime_indexer",
        level: str = "INFO",
        log_file: Optional[str] = None,
        format_string: Optional[str] = None
    ) -> logging.Logger:
        """
        Set up and configure a logger with console and optional file output.
        
        Args:
            name: Logger name
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: Optional path to log file
            format_string: Custom format string for log messages
        
        Returns:
            Configured logger instance
        """
        
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        
        # Prevent duplicate handlers
        if logger.handlers:
            logger.handlers.clear()
        
        # Default format
        if not format_string:
            format_string = (
                "%(asctime)s - %(name)s - %(levelname)s - "
                "%(filename)s:%(lineno)d - %(funcName)s() - %(message)s"
            )
        
        formatter = logging.Formatter(format_string)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, level.upper()))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler (optional)
        if log_file:
            # Ensure log directory exists
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(getattr(logging, level.upper()))
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        
        return logger
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """Get an existing logger by name."""
        return logging.getLogger(name)


def setup_application_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> logging.Logger:
    """
    Set up application-wide logging configuration.
    
    Args:
        log_level: The logging level to use
        log_file: Optional log file path
    
    Returns:
        The main application logger
    """
    
    # Setup main application logger
    main_logger = LoggerConfig.setup_logger(
        name="anime_indexer",
        level=log_level,
        log_file=log_file
    )
    
    # Setup loggers for different modules
    LoggerConfig.setup_logger(
        name="anime_indexer.domain",
        level=log_level,
        log_file=log_file
    )
    
    LoggerConfig.setup_logger(
        name="anime_indexer.infrastructure",
        level=log_level,
        log_file=log_file
    )
    
    LoggerConfig.setup_logger(
        name="anime_indexer.application",
        level=log_level,
        log_file=log_file
    )
    
    # Configure third-party loggers
    elasticsearch_logger = logging.getLogger("elasticsearch")
    elasticsearch_logger.setLevel(logging.WARNING)
    
    return main_logger
