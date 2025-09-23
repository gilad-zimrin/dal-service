from contextlib import asynccontextmanager
from typing import Type, Any, Optional
from pydantic import BaseModel
from asyncpg import Pool, Record, Connection

from src.dal.postgres_dal.sql_functions_model.base_sql_functions import BaseSQLFunctions


# TODO handle postgres exceptions
class BasePostgresDAL:
    """
    This is a subclass for an Item PostgresDal class, implements a generic version of base methods
    """
    def __init__(self, pool_or_conn: Pool | Connection, table_name: str, model: Type[BaseModel]):
        if not table_name or not model:
            raise ValueError("table_name and model are required.")
        self._pool_or_conn = pool_or_conn
        self.table = table_name
        self.model = model
        self.sql_functions: Optional[BaseSQLFunctions] = None

    @asynccontextmanager
    async def _get_conn(self, conn: Optional[Connection] = None):
        """
        Yield an asyncpg Connection.
        Usually we will acquire a new connection, unless we are working with an active transaction,
        in that case we will pass a single connection though multiple functions
        """
        if conn is not None:
            yield conn
            return

        # detect pool vs connection by 'acquire' attribute
        if hasattr(self._pool_or_conn, "acquire"):
            # it's a Pool
            async with self._pool_or_conn.acquire() as c:
                yield c
        else:
            # assume it is a Connection
            yield self._pool_or_conn

    async def create(self, data: dict[str, Any], conn: Optional[Connection] = None) -> BaseModel:
        """
        A base version of creating entity in postgres, will use a sql function if it exists
        :param data:
        :param conn:
        :return:
        """
        if self.sql_functions and self.sql_functions.create_function:
            async with self._get_conn(conn) as c:
                res = await self.sql_functions.call_create(c, data)
                return self.model(**res) if res else None

        cols = ", ".join(data.keys())
        placeholders = ", ".join(f"${i}" for i in range(1, len(data) + 1))
        query = f"INSERT INTO {self.table} ({cols}) VALUES ({placeholders}) RETURNING *"
        async with self._get_conn(conn) as c:
            row = await c.fetchrow(query, *data.values())
        return self.model(**dict(row)) if row else None

    async def get_all(self, conn: Optional[Connection] = None) -> list[BaseModel]:
        q = f"SELECT * FROM {self.table}"
        async with self._get_conn(conn) as c:
            rows = await c.fetch(q)
        return [self.model(**dict(r)) for r in rows]

    async def update(self, id_: Any, data: dict[str, Any], conn: Optional[Connection] = None) -> BaseModel | None:
        if self.sql_functions and self.sql_functions.update_function:
            async with self._get_conn(conn) as c:
                res = await self.sql_functions.call_update(c, id_, data)
                return self.model(**res) if res else None

        set_clause = ", ".join(f"{k}=${i+1}" for i, k in enumerate(data.keys()))
        query = f"UPDATE {self.table} SET {set_clause} WHERE id=${len(data) + 1} RETURNING *"
        async with self._get_conn(conn) as c:
            row = await c.fetchrow(query, *data.values(), id_)
        return self.model(**dict(row)) if row else None

    async def delete(self, id_: Any, conn: Optional[Connection] = None) -> bool:
        if self.sql_functions and self.sql_functions.delete_function:
            async with self._get_conn(conn) as c:
                res = await self.sql_functions.call_delete(c, id_)
                if isinstance(res, dict):
                    return True
                return bool(res)

        q = f"DELETE FROM {self.table} WHERE id=$1"
        async with self._get_conn(conn) as c:
            result = await c.execute(q, id_)
        return result.endswith("DELETE 1")

    async def execute_query(self, query: str, *args) -> list[Record]:
        """For custom queries. Must be parameterized!"""
        async with self._pool_or_conn.acquire() as conn:
            rows = await conn.fetch(query, *args)
        return rows
