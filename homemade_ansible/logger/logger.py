import logging
from .string_formatter import StringFormatter


class Logger:
    def __init__(self, is_debug=False):
        if is_debug:
            setup_debug()
        else:
            setup_logger()


# Configuration du logger de base, horodaté avec type de message, et message en question
def setup_logger():
    logFormatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logFormatter)

    logging.basicConfig(level=logging.INFO, handlers=[console_handler])

    error_handler = logging.StreamHandler()
    error_handler.setLevel(logging.ERROR)
    error_formatter = StringFormatter(max_length=200)
    error_handler.setFormatter(error_formatter)

    logging.getLogger().addHandler(error_handler)
    logging.getLogger("paramiko.transport.sftp").setLevel(logging.WARNING)


def setup_debug():
    logging.basicConfig(level=logging.DEBUG)

    paramiko_logger = logging.getLogger('paramiko')
    paramiko_logger.setLevel(logging.DEBUG)
