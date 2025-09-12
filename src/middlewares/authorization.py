from os import getenv

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import ORJSONResponse
from starlette.requests import Request

AUTH_HEADER = "Authorization"
EXPECTED_TOKEN = getenv("DAL_AUTH_TOKEN")

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get(AUTH_HEADER)
        if token != EXPECTED_TOKEN:
            return ORJSONResponse({"detail": "Unauthorized"}, status_code=401)
        return await call_next(request)
