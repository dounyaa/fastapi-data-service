import logging
import sys

from pythonjsonlogger import json as jsonlogger

from app.core.request_context import get_request_id
from app.core.settings import LogLevel


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = get_request_id()
        return True


_request_id_filter = RequestIdFilter()


def get_logger(name: str, level: LogLevel = LogLevel.INFO) -> logging.Logger:
    """Return a JSON-configured logger for the given name"""
    logger = logging.getLogger(name)
    mapped_level = level.to_logging_level()

    logger.setLevel(mapped_level)
    logger.propagate = False

    if logger.handlers:
        for h in logger.handlers:
            h.setLevel(mapped_level)
            if _request_id_filter not in h.filters:
                h.addFilter(_request_id_filter)
        return logger

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(mapped_level)
    handler.addFilter(_request_id_filter)

    handler.setFormatter(
        jsonlogger.JsonFormatter(
            "%(asctime)s %(name)s %(levelname)s [%(request_id)s] %(message)s",
            defaults={"request_id": "-"},
        )
    )

    logger.addHandler(handler)

    return logger
