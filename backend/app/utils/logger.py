import logging
import sys
from app.config import settings

def setup_logger(name: str = __name__) -> logging.Logger:
    """Setup logger with configuration"""
    logger = logging.getLogger(name)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    return logger

logger = setup_logger()

