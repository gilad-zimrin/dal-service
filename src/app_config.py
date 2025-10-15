from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, APIRouter
from fastapi.exceptions import ResponseValidationError, RequestValidationError, HTTPException

from core.postgres_db_pool import close_postgres_pool, initialize_postgres_pool
from src.core.exception_handlers import response_validation_exception_handler, http_exception_handler, \
    request_validation_exception_handler
from src.managers import ItemManager, ItemPostgresDAL, CustomerManager, CustomerPostgresDAL, CompanyManager, \
    CompanyPostgresDAL, OrderManager, OrderPostgresDAL
from src.middlewares.authorization import AuthMiddleware
from src.middlewares.error_catching import ErrorLoggingMiddleware
from src.routers import health_router, ItemRouter, CustomerRouter, CompanyRouter, OrderRouter

all_routers: List[APIRouter] = [
    health_router,
    ItemRouter(),
    CustomerRouter(),
    CompanyRouter(),
    OrderRouter()
]

# TODO create abstract class EntityConfig
def configure_routes(postgres_connection_pool):
    app.state.postgres_managers = {
        'Item': ItemManager(ItemPostgresDAL(postgres_connection_pool)),
        'Customer': CustomerManager(CustomerPostgresDAL(postgres_connection_pool)),
        'Company': CompanyManager(CompanyPostgresDAL(postgres_connection_pool)),
        'Order': OrderManager(
            OrderPostgresDAL(postgres_connection_pool), ItemManager(ItemPostgresDAL(postgres_connection_pool))
        )
    }
    [app.include_router(router) for router in all_routers]

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_postgres_pool(app)
    # add for each db

    configure_routes(app.state.postgres_pool)
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
