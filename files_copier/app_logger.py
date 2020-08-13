import logging


def _get_file_handler(log_file_path: str) -> logging.FileHandler:
    """
    Define parameters of logging in the file.

    Args:
        log_file_path (str): the path to the file for log messages write

    Returns:
        logging.FileHandler: file handler of the logger
    """
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s: %(message)s"),
    )
    return file_handler


def _get_stream_handler() -> logging.StreamHandler:
    """
    Define parameters of logging in the console.

    Returns:
        logging.StreamHandler: console handler of the logger.
    """
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(
        logging.Formatter("%(levelname)s: %(message)s"),
    )
    return stream_handler


def get_logger(name: str, log_file_path: str) -> logging.Logger:
    """
    Define all parameters of logging.

    Args:
        name (str): name of the logger.
        log_file_path (str): the path to the file for log messages write.

    Returns:
        logging.Logger: logger with specified parameters.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(_get_file_handler(log_file_path))
    logger.addHandler(_get_stream_handler())
    return logger
