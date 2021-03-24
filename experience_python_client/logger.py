import logging

def log():
    loggers = logging.getLogger(__name__)
    loggers.setLevel(logging.DEBUG)
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    file_handler = logging.FileHandler('reportapi.log')
    file_handler.setFormatter(formatter)
    loggers.addHandler(file_handler)
    return loggers