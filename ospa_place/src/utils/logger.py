import sys
import logging


class Logger:
    """Centralized logger class for the application"""

    _instance = None
    _initialized = False

    def __new__(cls):
        """Singleton pattern to ensure only one logger instance"""
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize logger configuration only once"""
        if not self._initialized:
            self._setup_logging()
            Logger._initialized = True

    def _setup_logging(self):
        """Configure root logger once for entire application"""
        self.root_logger = logging.getLogger()
        self.level = logging.INFO
        self.root_logger.setLevel(self.level)

        # Remove existing handlers to avoid duplicates
        if self.root_logger.handlers:
            self.root_logger.handlers.clear()

        # Create console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.level)

        # Format with module name
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(formatter)
        self.root_logger.addHandler(console_handler)

        self.root_logger.info(f"Logging configured level={self.level}")

    def get_logger(self, name: str = None) -> logging.Logger:
        """Get a logger instance for a specific module"""
        if name:
            return logging.getLogger(name)
        return self.root_logger
