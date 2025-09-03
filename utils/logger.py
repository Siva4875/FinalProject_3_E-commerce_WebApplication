import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class Logger:
    """
    A custom logger class that sets up both console and file logging.
    Uses rotating file handler to prevent oversized log files.
    """
    def __init__(self, name=__name__, log_level=logging.INFO):
        # Create logger instance
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # Clear existing handlers to avoid duplicate logs if re-initialized
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # Create 'logs' directory (project_root/logs) if it doesn't exist
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
        os.makedirs(log_dir, exist_ok=True)
        
        # Define formatters
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        
        # Console handler for live log display in terminal
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(console_formatter)
        
        # File handler with log rotation (to prevent unlimited log size)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(log_dir, f"test_execution_{timestamp}.log")
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # Each log file max size: 10MB
            backupCount=5,          # Keep up to 5 backup log files
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(file_formatter)
        
        # Add handlers to logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def get_logger(self):
        """Return the configured logger instance."""
        return self.logger


def setup_logging(log_level=logging.INFO):
    """
    Set up a root logger configuration for global logging.
    
    - Creates 'logs' directory if it doesn't exist.
    - Configures console + rotating file handlers.
    - Can be called once in test framework setup.
    """
    # Create logs directory at project root
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear any existing handlers to avoid duplicate logs
    if root_logger.handlers:
        root_logger.handlers.clear()
    
    # Define formatters
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)
    
    # File handler with daily log file rotation
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = os.path.join(log_dir, f"automation_{timestamp}.log")
    
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB max size
        backupCount=7,          # Keep logs for 7 days
        encoding='utf-8'
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(file_formatter)
    
    # Add both handlers to root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    return root_logger


# Global logger instance (can be imported across framework)
logger = Logger(__name__).get_logger()


if __name__ == "__main__":
    # Test the logger functionality
    logger.info("Logger configuration test - INFO level")
    logger.debug("Logger configuration test - DEBUG level")
    logger.warning("Logger configuration test - WARNING level")
    logger.error("Logger configuration test - ERROR level")
