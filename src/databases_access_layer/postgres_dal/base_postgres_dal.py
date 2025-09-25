from contextlib import asynccontextmanager
from typing import Type, Any, Optional, TypeVar

from asyncpg import Pool, Record, Connection
from pydantic import BaseModel

from src.databases_access_layer.postgres_dal.sql_functions_model.base_sql_functions import BaseSQLFunctions


# TODO handle postgres exceptions
class BasePostgresDAL:
    """
    This is a subclass for an Item PostgresDal class, implements a generic version of base methods
    """
    def __init__(
            self,
            pool_or_conn: Pool | Connection,
            table_name: str, model: Type[BaseModel],
            schema_name: str
    ):
        if not table_name or not model:
            raise ValueError("table_name and model are required.")
        self._pool_or_conn = pool_or_conn
        self.table = table_name
        self.model = model
        self.schema_name = schema_name
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

        if hasattr(self._pool_or_conn, "acquire"):
            async with self._pool_or_conn.acquire() as c:
                yield c
        else:
            yield self._pool_or_conn

    async def create(self, data: dict[str, Any], conn: Optional[Connection] = None) -> dict[str, Any]:
        """
        A base version of creating entity in postgres, will use a sql function if it exists
        :param data:
        :param conn:
        :return:
        """
        if not self.sql_functions or not self.sql_functions.create_function:
            raise NotImplementedError("A create function is not implemented for the model")

        async with self._get_conn(conn) as connection:
            response = await self.sql_functions.call_create(connection, data)
            return response


    async def get_by_id(
            self, object_id: str | int, field_name: str, conn: Optional[Connection] = None
    ) -> dict | dict[str, Any]:
        query = f"SELECT * FROM {self.schema_name}.{self.table} WHERE {field_name} = {object_id}"
        async with self._get_conn(conn) as connection:
            rows = await connection.fetch(query)
            if len(rows) > 1:
                raise ValueError(f"Field {field_name} in not unique on table {self.schema_name}.{self.table}")
        return dict(rows[0])

    async def get_all(self, conn: Optional[Connection] = None) -> list[dict | dict[str, Any]]:
        query = f"SELECT * FROM {self.schema_name}.{self.table}"
        async with self._get_conn(conn) as connection:
            rows = await connection.fetch(query)
        return [dict(r) for r in rows]

    async def update(self, id_: Any, data: dict[str, Any], conn: Optional[Connection] = None) -> BaseModel | None:
        if not self.sql_functions or not self.sql_functions.update_function:
            raise NotImplementedError("An update function is not implemented for the model")

        async with self._get_conn(conn) as connection:
            response = await self.sql_functions.call_update(connection, id_, data)
            return response

    async def delete(self, id_: Any, conn: Optional[Connection] = None) -> bool:
        if not self.sql_functions or not self.sql_functions.delete_function:
            raise NotImplementedError("A delete function is not implemented for the model")
        
        async with self._get_conn(conn) as connection:
            res = await self.sql_functions.call_delete(connection, id_)
            if isinstance(res, dict):
                return True
            return bool(res)

    async def execute_query(self, query: str, *args) -> list[Record]:
        """For custom queries. Must be parameterized!"""
        async with self._pool_or_conn.acquire() as connection:
            rows = await connection.fetch(query, *args)
        return rows

DALType = TypeVar("DALType", bound=BasePostgresDAL)
