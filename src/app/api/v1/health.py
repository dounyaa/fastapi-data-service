from fastapi import APIRouter

from app.core.logger import get_logger
from app.schemas.health import HealthResponse

router = APIRouter(tags=["system"])
logger = get_logger(__name__)


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    """Liveness health check endpoint"""
    logger.info("Health check called")
    return HealthResponse(status="ok")
