import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.anyio
async def test_demo_error_returns_expected_response() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/demo-error")
    assert response.status_code == 418
    assert response.json() == {
        "error": {
            "code": "DEMO_ERROR",
            "message": "Demo error",
        }
    }
