from fastapi import Request, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from src.core.logger import get_logger

logger = get_logger("errors")


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    route_path = request.url.path
    func_name = getattr(request.scope.get("endpoint"), "__name__", "unknown")
    logger.exception(f"Validation error on {route_path} in {func_name}", exc_info=True)
    return ORJSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    route_path = request.url.path
    func_name = getattr(request.scope.get("endpoint"), "__name__", "unknown")
    logger.exception(f"HTTP error on {route_path} in {func_name}", exc_info=True)
    return ORJSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


async def unhandled_exception_handler(request: Request, exc: Exception):
    route_path = request.url.path
    func_name = getattr(request.scope.get("endpoint"), "__name__", "unknown")
    logger.exception(f"Unhandled error on {route_path} in {func_name}", exc_info=True)
    return ORJSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
