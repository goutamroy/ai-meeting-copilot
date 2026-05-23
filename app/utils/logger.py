import logging
import sys


def setup_logger() -> logging.Logger:
    logger = logging.getLogger(
        "ai_meeting_copilot"
    )

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )

    console_handler = (
        logging.StreamHandler(
            sys.stdout
        )
    )
    console_handler.setFormatter(
        formatter
    )

    logger.addHandler(
        console_handler
    )

    logger.propagate = False

    return logger


logger = setup_logger()


def log_with_request_id(
    request_id: str,
    level: str,
    message: str
):
    formatted_message = (
        f"[request_id={request_id}] "
        f"{message}"
    )

    if level == "info":
        logger.info(
            formatted_message
        )

    elif level == "warning":
        logger.warning(
            formatted_message
        )

    elif level == "error":
        logger.error(
            formatted_message
        )

    else:
        logger.info(
            formatted_message
        )