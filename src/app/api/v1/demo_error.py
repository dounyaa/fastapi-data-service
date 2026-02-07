from fastapi import APIRouter

from app.core.errors import AppError

router = APIRouter(tags=["debug"])


@router.get("/demo-error")
def demo_error() -> None:
    """demo_error endpoint temporary for testing module error handling"""
    raise AppError(
        message="Demo error",
        code="DEMO_ERROR",
        status_code=418,
    )
