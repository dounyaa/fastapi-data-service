import logging
from enum import Enum
from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Environment(str, Enum):
    DEV = "dev"
    STAGING = "staging"
    PROD = "prod"


class LogLevel(str, Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

    def to_logging_level(self) -> int:
        match self:
            case LogLevel.DEBUG:
                return logging.DEBUG
            case LogLevel.INFO:
                return logging.INFO
            case LogLevel.WARNING:
                return logging.WARNING
            case LogLevel.ERROR:
                return logging.ERROR
            case LogLevel.CRITICAL:
                return logging.CRITICAL


class Settings(BaseSettings):
    app_name: str = Field(default="fastapi-data-service")
    app_version: str = Field(default="0.1.0")
    environment: Environment = Field(default=Environment.DEV)
    api_prefix: str = Field(default="/api/v1")
    log_level: LogLevel = Field(default=LogLevel.INFO)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return cached settings object."""
    return Settings()
