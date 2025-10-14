from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import ORJSONResponse
from starlette.requests import Request

from src.core.logger import get_logger

logger = get_logger("errors")

async def response_validation_exception_handler(request: Request, exc: ResponseValidationError):
    route_path = request.url.path
    route_handler = request.scope.get("endpoint")
    func_name = getattr(route_handler, "__name__", "unknown")

    logger.exception(
        f"Response Validation error on {route_path} in {func_name}",
        exc_info=True, extra={"error": exc.errors()}
    )
    return ORJSONResponse(
        status_code=422,  # Standard HTTP status code for validation errors
        content={"detail": "Response validation failed", "errors": [
        {
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"],
        }
        for error in exc.errors()
    ]},
    )

async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    route_path = request.url.path
    route_handler = request.scope.get("endpoint")
    func_name = getattr(route_handler, "__name__", "unknown")

    logger.exception(
        f"Request Validation error on {route_path} in {func_name}",
        exc_info=True,
    )
    return ORJSONResponse(
        status_code=422,  # Standard HTTP status code for validation errors
        content={"detail": "Request validation failed", "errors": [
        {
            "loc": error["loc"],
            "msg": error["msg"],
            "type": error["type"],
        }
        for error in exc.errors()
    ]},
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    route_path = request.url.path
    func_name = getattr(request.scope.get("endpoint"), "__name__", "unknown")
    logger.exception(f"HTTP error on {route_path} in {func_name}", exc_info=True)
    return ORJSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
