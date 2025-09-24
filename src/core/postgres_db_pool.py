from os import getenv
from dotenv import load_dotenv
import asyncpg
from fastapi import FastAPI, Request

from src.core.logger import logger

load_dotenv()

postgres_connection_pool: asyncpg.pool.Pool | None = None

async def initialize_postgres_pool(
    app: FastAPI,
    *,
    min_size: int = int(getenv("POSTGRES_POOL_MIN_SIZE", default=1)),
    max_size: int = int(getenv("POSTGRES_POOL_MAX_SIZE", default=10)),
):
    """Initialize asyncpg connection pool using environment variables."""
    global postgres_connection_pool

    user = getenv("POSTGRES_USERNAME")
    password = getenv("POSTGRES_PASSWORD")
    database = getenv("POSTGRES_DB")
    host = getenv("POSTGRES_HOST", "127.0.0.1")
    port = int(getenv("POSTGRES_PORT", 5432))

    postgres_connection_pool = await asyncpg.create_pool(
        user=user,
        password=password,
        database=database,
        host=host,
        port=port,
        min_size=min_size,
        max_size=max_size,
    )
    app.state.postgres_pool = postgres_connection_pool
    logger.info("Created postgres connection pool")

async def close_postgres_pool(app: FastAPI):
    """Close the asyncpg pool on shutdown."""
    global postgres_connection_pool
    if postgres_connection_pool:
        await postgres_connection_pool.close()

async def get_postgres_pool(request: Request):
    return request.app.state.postgres_pool
