import logging

def get_logger():
    logger = logging.getLogger("automation")
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler("reports/test.log")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger