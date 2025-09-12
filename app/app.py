from fastapi import FastAPI

from app.middlewares.authorization import AuthMiddleware
from app.middlewares.error_handling import ErrorLoggingMiddleware

app = FastAPI(title="DAL Service")

app.add_middleware(AuthMiddleware)
app.add_middleware(ErrorLoggingMiddleware)

