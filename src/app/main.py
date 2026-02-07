from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.v1.crash import router as crash_router
from app.api.v1.demo_error import router as error_router
from app.api.v1.echo import router as echo_router
from app.api.v1.health import router as health_router
from app.core.errors import AppError
from app.core.logger import get_logger
from app.core.middlewares.request_id import request_id_middleware
from app.core.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    logger = get_logger(settings.app_name, settings.log_level)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        logger.info("Application startup")
        yield
        logger.info("Application shutdown")

    app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)
    app.middleware("http")(request_id_middleware)

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        logger.warning(
            "code=%s message=%s path=%s method=%s",
            exc.code,
            exc.message,
            request.url.path,
            request.method,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                }
            },
        )

    @app.exception_handler(RequestValidationError)
    async def app_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        logger.warning(
            "path=%s method=%s nbErrors=%i errors_preview=%s",
            request.url.path,
            request.method,
            len(exc.errors()),
            exc.errors()[:5],
        )
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "details": exc.errors(),
                }
            },
        )

    @app.exception_handler(Exception)
    async def app_internal_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        logger.exception(
            "path=%s method=%s",
            request.url.path,
            request.method,
        )
        return JSONResponse(
            status_code=500,
            content={"error": {"code": "INTERNAL_ERROR", "message": "Internal server error"}},
        )

    app.include_router(health_router, prefix=settings.api_prefix)
    app.include_router(error_router, prefix=settings.api_prefix)
    app.include_router(echo_router, prefix=settings.api_prefix)
    app.include_router(crash_router, prefix=settings.api_prefix)

    return app


app = create_app()
