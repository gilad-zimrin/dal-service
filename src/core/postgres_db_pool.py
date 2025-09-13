from os import getenv
from dotenv import load_dotenv
import asyncpg
from fastapi import FastAPI

load_dotenv()

pool: asyncpg.pool.Pool | None = None

async def initialize_postgres_pool(
    app: FastAPI,
    *,
    min_size: int = int(getenv("POSTGRES_POOL_MIN_SIZE", default=1)),
    max_size: int = int(getenv("POSTGRES_POOL_MAX_SIZE", default=10)),
):
    """Initialize asyncpg connection pool using environment variables."""
    global pool

    user = getenv("POSTGRES_USERNAME")
    password = getenv("POSTGRES_PASSWORD")
    database = getenv("POSTGRES_DB")
    host = getenv("POSTGRES_HOST", "127.0.0.1")
    port = int(getenv("POSTGRES_PORT", 5432))

    pool = await asyncpg.create_pool(
        user=user,
        password=password,
        database=database,
        host=host,
        port=port,
        min_size=min_size,
        max_size=max_size,
    )
    app.state.db_pool = pool
async def close_postgres_pool(app: FastAPI):
    """Close the asyncpg pool on shutdown."""
    global pool
    if pool:
        await pool.close()
