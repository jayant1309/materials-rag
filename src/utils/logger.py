import sys
from loguru import logger

def setup_logger(log_level: str = "INFO") -> None:
    """
    Configures the global logger with a standard format.
    
    Args:
        log_level: The logging level to use (e.g., DEBUG, INFO, ERROR).
    """
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=log_level,
    )
    logger.add(
        "logs/app.log",
        rotation="10 MB",
        retention="1 month",
        level="DEBUG",
        compression="zip",
    )

# Initial setup with default level
setup_logger()
