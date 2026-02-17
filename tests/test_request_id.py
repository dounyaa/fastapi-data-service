import logging

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

REQUEST_ID_HEADER = "X-Request-ID"


@pytest.mark.anyio
async def test_request_id_generation() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/health")

    assert REQUEST_ID_HEADER in response.headers
    rid = response.headers[REQUEST_ID_HEADER]
    assert rid
    assert len(rid) == 32


@pytest.mark.anyio
async def test_request_id_propagation() -> None:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/health", headers={REQUEST_ID_HEADER: "abc123"})

    assert response.headers[REQUEST_ID_HEADER] == "abc123"


@pytest.mark.anyio
async def test_request_id_logs(caplog) -> None:
    logger = logging.getLogger("app.api.v1.health")

    logger.addHandler(caplog.handler)
    caplog.set_level(logging.INFO, logger=logger.name)

    try:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.get("/api/v1/health")

        rid = response.headers[REQUEST_ID_HEADER]

        assert any(
            r.request_id == rid and "Health check called" in r.message for r in caplog.records
        )

    finally:
        logger.removeHandler(caplog.handler)
