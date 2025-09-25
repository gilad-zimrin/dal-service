from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, APIRouter
from fastapi.exceptions import ResponseValidationError, RequestValidationError, HTTPException

from core.postgres_db_pool import close_postgres_pool, initialize_postgres_pool
from routers.health import health_router
from src.core.exception_handlers import response_validation_exception_handler, http_exception_handler, \
    request_validation_exception_handler
from src.databases_access_layer.postgres_dal.item_dal import ItemPostgresDAL
from src.databases_access_layer.postgres_dal.user_dal import UserPostgresDAL
from src.managers.item_manager import ItemManager
from src.managers.user_manager import UserManager
from src.middlewares.authorization import AuthMiddleware
from src.middlewares.error_catching import ErrorLoggingMiddleware

from src.routers.item_router import ItemRouter
from src.routers.user_router import UserRouter


def routers_registration():
    [app.include_router(router) for router in all_routers]


def set_app_managers(postgres_connection_pool):
    app.state.postgres_managers = {
        'Item': ItemManager(ItemPostgresDAL(postgres_connection_pool)),
        'User': UserManager(UserPostgresDAL(postgres_connection_pool))
    }


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_postgres_pool(app)
    # add for each db
    set_app_managers(app.state.postgres_pool)

    routers_registration()
    yield

    await close_postgres_pool(app)

# TODO override the default fastapi logs with my custom logs
# TODO support get certain fields
# TODO support generic filtering (AND, OR, EQUALS)
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
