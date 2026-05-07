import logging
import os

# Factory function to initialize and return a configured logger instance
def get_logger():
    # Ensure reports directory exists for storing log files
    os.makedirs("reports", exist_ok=True)

    # Create/retrieve a named logger for the automation framework
    logger = logging.getLogger("automation")

    # ⭐ Prevent duplicate handlers during parallel execution or repeated imports
    # This avoids multiple log entries for the same event
    if logger.hasHandlers():
        logger.handlers.clear()

    # Set logging level to INFO for standard runtime visibility
    logger.setLevel(logging.INFO)

    # File handler to persist logs into a file inside reports directory
    handler = logging.FileHandler("reports/test.log", mode="a")

    # Define log format: timestamp, log level, and actual message
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Attach formatter to handler for structured log output
    handler.setFormatter(formatter)

    # Attach handler to logger instance
    logger.addHandler(handler)

    # Return configured logger for use across framework
    return logger