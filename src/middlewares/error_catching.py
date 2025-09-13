from fastapi.responses import ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from src.core.logger import get_logger

logger = get_logger("errors")


class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except (Exception,) as err:
            route_path = request.url.path
            route_handler = request.scope.get("endpoint")
            func_name = getattr(route_handler, "__name__", "unknown")

            logger.exception(
                f"An unexpected error occurred on {route_path} in {func_name}",
            )
            return ORJSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )

