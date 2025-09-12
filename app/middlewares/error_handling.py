from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException

from app.utils.logger import get_logger

log = get_logger("errors")

class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except RequestValidationError as ve:
            route_path = request.url.path
            route_handler = request.scope.get("endpoint")
            func_name = getattr(route_handler, "__name__", "unknown")

            log.exception(
                f"Validation error on {route_path} in {func_name}",
                exc_info=True,
            )
            return ORJSONResponse(
                status_code=422,
                content={
                    "detail": ve.errors(),
                    "body": ve.body,
                },
            )
        except HTTPException as he:
            route_path = request.url.path
            route_handler = request.scope.get("endpoint")
            func_name = getattr(route_handler, "__name__", "unknown")

            log.exception(
                f"HTTP error on {route_path} in {func_name}",
                exc_info=True,
            )
            return ORJSONResponse(
                status_code=he.status_code,
                content={"detail": he.detail},
            )
        except (Exception,):
            route_path = request.url.path
            route_handler = request.scope.get("endpoint")
            func_name = getattr(route_handler, "__name__", "unknown")

            log.exception(
                f"Unhandled error on {route_path} in {func_name}",
                exc_info=True,
            )
            return ORJSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )
