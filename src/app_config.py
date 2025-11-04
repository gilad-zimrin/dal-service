from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import ResponseValidationError, RequestValidationError, HTTPException

from core.postgres_db_pool import close_postgres_pool, initialize_postgres_pool
from src.core.exception_handlers import response_validation_exception_handler, http_exception_handler, \
    request_validation_exception_handler
from src.entities import AdminEntity, CompanyEntity, CustomerEntity, ItemEntity, OrderEntity
from src.middlewares.authorization import AuthMiddleware
from src.middlewares.error_catching import ErrorLoggingMiddleware
from src.routers import health_router
from src.routers.auth_router import security_router

all_entities = [
    ItemEntity(),
    CompanyEntity(),
    CustomerEntity(),
    OrderEntity(),
    AdminEntity()
]

def configure_entities_to_app(postgres_connection_pool):
    """
    This function configures all entities into the fastapi app
    :param postgres_connection_pool:
    :return:
    """
    app.include_router(health_router)
    app.include_router(security_router)

    app.state.postgres_managers = {}
    for entity in all_entities:
        app.state.postgres_managers[entity.entity_name] = entity.get_manager(postgres_connection_pool)
        app.include_router(entity.entity_router())

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_postgres_pool(app)
    # add for each db

    configure_entities_to_app(app.state.postgres_pool)
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
