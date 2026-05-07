import logging
import os

def get_logger():
    os.makedirs("reports", exist_ok=True)

    logger = logging.getLogger("automation")

    # ⭐ PREVENT DUPLICATE HANDLERS (IMPORTANT FOR PARALLEL RUN)
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.INFO)

    handler = logging.FileHandler("reports/test.log", mode="a")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger