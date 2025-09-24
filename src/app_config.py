from contextlib import asynccontextmanager
from os import getenv
from typing import List

from fastapi import FastAPI, APIRouter
from fastapi.exceptions import ResponseValidationError, RequestValidationError, HTTPException

from core.postgres_db_pool import close_postgres_pool, initialize_postgres_pool
from routers.health import health_router
from src.core.exception_handlers import response_validation_exception_handler, http_exception_handler, \
    request_validation_exception_handler
from src.middlewares.authorization import AuthMiddleware
from src.middlewares.error_catching import ErrorLoggingMiddleware
from src.routers.item_router import ItemRouter
from src.routers.user_router import UserRouter


def routers_registration():
    [app.include_router(router) for router in all_routers]

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_postgres_pool(app)
    # add for each db

    routers_registration()
    yield

    await close_postgres_pool(app)

# TODO override the default fastapi logs with my custom logs
app = FastAPI(title="Async DAL Service", version="0.1.0", lifespan=lifespan)

app.add_middleware(AuthMiddleware)
app.add_middleware(ErrorLoggingMiddleware)

app.add_exception_handler(RequestValidationError, request_validation_exception_handler) # type: ignore[arg-type]
app.add_exception_handler(ResponseValidationError, response_validation_exception_handler) # type: ignore[arg-type]
app.add_exception_handler(HTTPException, http_exception_handler) # type: ignore[arg-type]

all_routers: List[APIRouter] = [
    health_router,
    ItemRouter(),
    UserRouter()
]
