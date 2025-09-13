import asyncpg
from fastapi import FastAPI

pool: asyncpg.Pool | None = None

async def initialize_postgres_pool(app: FastAPI, dsn: str):
    """Initialize asyncpg connection pool on startup."""
    global pool
    pool = await asyncpg.create_pool(dsn)
    app.state.db_pool = pool

async def close_postgres_pool(app: FastAPI):
    """Close the asyncpg pool on shutdown."""
    global pool
    if pool:
        await pool.close()
