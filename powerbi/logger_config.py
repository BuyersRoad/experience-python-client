import logging



def powerBI_log():
    LOG_PATH =  'powerBI.log'
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setFormatter(formatter)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(file_handler)
    return logger