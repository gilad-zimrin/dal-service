import time

from fastapi import FastAPI, Request, Response, status
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, max_requests: int, window_size: int):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_size = window_size
        self.ip_request_log = {}

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        if client_ip not in self.ip_request_log:
            self.ip_request_log[client_ip] = []

        request_times = [
            timestamp for timestamp in self.ip_request_log[client_ip]
            if current_time - timestamp < self.window_size
        ]
        self.ip_request_log[client_ip] = request_times

        if len(request_times) >= self.max_requests:
            return Response(
                content="Too many requests. Please try again later.",
                status_code=status.HTTP_429_TOO_MANY_REQUESTS
            )

        self.ip_request_log[client_ip].append(current_time)

        return await call_next(request)
