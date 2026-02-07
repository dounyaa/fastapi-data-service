from fastapi import APIRouter

router = APIRouter(tags=["debug"])


@router.get("/crash")
def demo_crash() -> None:
    """demo_crash endpoint temporary for testing module internal error handling"""
    raise RuntimeError("boom")
