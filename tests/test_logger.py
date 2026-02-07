import logging

import pytest

from app.core.logger import get_logger
from app.core.settings import LogLevel


@pytest.fixture
def reset_logger():
    created: set[str] = set()

    def _reset(name: str) -> None:
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.setLevel(logging.NOTSET)
        logger.propagate = True
        created.add(name)

    yield _reset

    for name in created:
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.setLevel(logging.NOTSET)
        logger.propagate = True


def test_logger_level(reset_logger) -> None:
    reset_logger("x")
    logger_x = get_logger("x", LogLevel.INFO)
    assert logger_x.level == logging.INFO
    assert len(logger_x.handlers) == 1
    assert logger_x.handlers[0].level == logging.INFO

    reset_logger("y")
    logger_y = get_logger("y", LogLevel.DEBUG)
    assert logger_y.level == logging.DEBUG
    assert len(logger_y.handlers) == 1
    assert logger_y.handlers[0].level == logging.DEBUG


def test_logger_level_update(reset_logger) -> None:
    reset_logger("x")

    logger1 = get_logger("x", LogLevel.INFO)
    logger2 = get_logger("x", LogLevel.DEBUG)

    assert logger1 is logger2
    assert logger2.level == logging.DEBUG
    assert len(logger2.handlers) == 1
    assert logger2.handlers[0].level == logging.DEBUG
