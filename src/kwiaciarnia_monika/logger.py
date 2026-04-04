import logging


def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        filename="main.log",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)
