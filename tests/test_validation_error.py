import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.anyio
async def test_echo_invalid_payload() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/echo", json={"text": "", "count": 0})
    assert response.status_code == 422
    data = response.json()
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert data["error"]["message"] == "Request validation failed"
    assert len(data["error"]["details"]) > 0


@pytest.mark.anyio
async def test_echo_valid_payload() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/api/v1/echo", json={"text": "hi", "count": 3})
    assert response.status_code == 200
    assert response.json() == {"result": "hi hi hi"}
