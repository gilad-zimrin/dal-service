from fastapi import FastAPI

from src.middlewares.authorization import AuthMiddleware
from src.middlewares.error_handling import ValidationErrorMiddleware

app = FastAPI(title="DAL Service")

app.add_middleware(AuthMiddleware)
app.add_middleware(ValidationErrorMiddleware)

