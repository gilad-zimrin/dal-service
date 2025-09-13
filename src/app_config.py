from contextlib import asynccontextmanager
from os import getenv
from typing import List

from fastapi import FastAPI, APIRouter
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError

from core.postgres_db_pool import close_postgres_pool
from routers.health import health_router
from src.core.error_handling import http_exception_handler, validation_exception_handler, unhandled_exception_handler
from src.middlewares.authorization import AuthMiddleware
from src.routers.item_router import ItemRouter
from src.routers.user_router import UserRouter

postgres_connection_string = getenv("POSTGRES_CONNECTION_STRING")

def routers_registration():
    [app.include_router(router) for router in all_routers]

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await initialize_postgres_pool(app, dsn=postgres_connection_string)
    # add for each db

    routers_registration()
    yield

    await close_postgres_pool(app)

app = FastAPI(title="Async DAL Service", version="0.1.0", lifespan=lifespan)

app.add_exception_handler(RequestValidationError, validation_exception_handler) # type: ignore[override]
app.add_exception_handler(HTTPException, http_exception_handler) # type: ignore[override]
app.add_exception_handler(Exception, unhandled_exception_handler)

app.add_middleware(AuthMiddleware)

all_routers: List[APIRouter] = [health_router, ItemRouter(), UserRouter()]
