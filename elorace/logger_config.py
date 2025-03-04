import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def get_logger(name = __name__):
    LOG_DIR = "logs"
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  

    if not logger.handlers:
        log_filename = os.path.join(LOG_DIR, f"elorace_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = RotatingFileHandler(
            log_filename,
            maxBytes=10485760,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)


    return logger

# Test del logger
if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.info("Test log message")
    logger.error("Test error message")
