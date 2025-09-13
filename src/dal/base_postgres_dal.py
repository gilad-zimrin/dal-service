from typing import Type, Any
from pydantic import BaseModel
from asyncpg import Pool, Record

class BasePostgresDAL:
    """
    This is a subclass for an Item PostgresDal class, implements a generic version of base methods
    """
    def __init__(self, pool: Pool, table_name: str, model: Type[BaseModel]):
        if not table_name or not model:
            raise ValueError("table_name and model are required.")
        self.pool = pool
        self.table = table_name
        self.model = model

    async def create(self, data: dict[str, Any]) -> BaseModel:
        """
        A basic implementation of create function
        :param data:
        :return:
        """
        cols = ", ".join(data.keys())
        placeholders = ", ".join(f"${i}" for i in range(1, len(data) + 1))
        query = f"INSERT INTO {self.table} ({cols}) VALUES ({placeholders}) RETURNING *"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *data.values())
        return self.model(**dict(row))

    async def get(self, id_: Any) -> BaseModel | None:
        query = f"SELECT * FROM {self.table} WHERE id=$1"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, id_)
        return self.model(**dict(row)) if row else None

    async def get_all(self) -> list[BaseModel]:
        query = f"SELECT * FROM {self.table}"
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query)
        return [self.model(**dict(r)) for r in rows]

    async def update(self, id_: Any, data: dict[str, Any]) -> BaseModel | None:
        set_clause = ", ".join(f"{k}=${i+1}" for i, k in enumerate(data.keys()))
        query = f"UPDATE {self.table} SET {set_clause} WHERE id=${len(data)+1} RETURNING *"
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *data.values(), id_)
        return self.model(**dict(row)) if row else None

    # TODO think or how to not implement delete
    async def delete(self, id_: Any) -> bool:
        query = f"DELETE FROM {self.table} WHERE id=$1"
        async with self.pool.acquire() as conn:
            result = await conn.execute(query, id_)
        return result.endswith("DELETE 1")

    async def execute_query(self, query: str, *args) -> list[Record]:
        """For custom queries. Must be parameterized!"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *args)
        return rows
