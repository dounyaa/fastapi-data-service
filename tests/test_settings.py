import pytest
from pydantic import ValidationError

from app.core.settings import get_settings


@pytest.fixture(autouse=True)
def clear_settings_cache():
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_default_settings() -> None:
    s = get_settings()
    assert s.app_name == "fastapi-data-service"
    assert s.app_version == "0.1.0"
    assert s.api_prefix == "/api/v1"
    assert s.environment.value == "dev"
    assert s.log_level.value == "INFO"


def test_override_settings(monkeypatch) -> None:
    monkeypatch.setenv("APP_NAME", "x")
    monkeypatch.setenv("API_PREFIX", "/api/v2")

    get_settings.cache_clear()
    s = get_settings()
    assert s.app_name == "x"
    assert s.api_prefix == "/api/v2"


def test_invalid_env(monkeypatch) -> None:
    monkeypatch.setenv("ENVIRONMENT", "invalid")
    get_settings.cache_clear()

    with pytest.raises(ValidationError):
        get_settings()
