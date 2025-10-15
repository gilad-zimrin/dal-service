from contextlib import asynccontextmanager
from string import Template
from typing import Any, Optional, TypeVar

from asyncpg import Pool, Record, Connection
from pydantic import BaseModel

from src.core.exceptions.object_not_found_error import ObjectNotFoundError
from src.databases_access_layer.postgres_dal.functions_model.base_sql_functions import BaseSQLFunctions


# TODO handle postgres exceptions
class BasePostgresDAL:
    """
    This is a subclass for an Item PostgresDal class, implements a generic version of base methods
    """
    def __init__(
            self,
            pool_or_conn: Pool | Connection,
            table_name: str,
            schema_name: str
    ):
        if not table_name:
            raise ValueError("table_name is required.")
        self._pool_or_conn = pool_or_conn
        self.table = table_name
        self.schema_name = schema_name
        self.sql_functions: Optional[BaseSQLFunctions] = None
        self.get_by_id_query: str = ''
        self.get_all_query: str = ''

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
            self, object_id: str | int, unique_field_name: str, conn: Optional[Connection] = None
    ) -> dict | dict[str, Any]:

        get_by_id_query = Template(self.get_by_id_query).substitute({"object_id": object_id}) \
            if self.get_by_id_query \
            else f"SELECT * FROM {self.schema_name}.{self.table} WHERE {unique_field_name} = {object_id}"

        async with self._get_conn(conn) as connection:
            rows = await connection.fetch(get_by_id_query)
            if len(rows) > 1:
                raise ValueError(f"Field {unique_field_name} in not unique on table {self.schema_name}.{self.table}")
            if len(rows) == 0:
                raise ObjectNotFoundError(
                    f'An object with id {object_id} not found on table {self.schema_name}.{self.table}'
                )
        return dict(rows[0])

    async def get_all(self, conn: Optional[Connection] = None) -> list[dict | dict[str, Any]]:
        get_all_query = self.get_all_query if self.get_all_query else f"SELECT * FROM {self.schema_name}.{self.table}"
        async with self._get_conn(conn) as connection:
            rows = await connection.fetch(get_all_query)

        return [dict(r) for r in rows]

    async def update(self, id_: Any, data: dict[str, Any], conn: Optional[Connection] = None) -> dict[str, Any] | None:
        if not self.sql_functions or not self.sql_functions.update_function:
            raise NotImplementedError("An update function is not implemented for the model")

        async with self._get_conn(conn) as connection:
            response = await self.sql_functions.call_update(connection, id_, data)
            # TODO raise an error when updating what doesnt exists
            return response

    async def delete(self, id_: Any, conn: Optional[Connection] = None) -> bool:
        if not self.sql_functions or not self.sql_functions.delete_function:
            raise NotImplementedError("A delete function is not implemented for the model")
        
        async with self._get_conn(conn) as connection:
            res = await self.sql_functions.call_delete(connection, id_)
            if isinstance(res, dict):
                return True
            # TODO raise an error when deleting what doesnt exists
            return bool(res)

    async def execute_query(self, query: str, *args) -> list[Record]:
        """For custom queries. Must be parameterized!"""
        async with self._pool_or_conn.acquire() as connection:
            rows = await connection.fetch(query, *args)
        return rows

DALType = TypeVar("DALType", bound=BasePostgresDAL)
