from os import getenv

from asyncpg import Pool, Connection

from src.databases_access_layer.postgres_dal.base_postgres_dal import BasePostgresDAL
from src.databases_access_layer.postgres_dal.functions_model.item_sql_functions import ItemSQLFunctions

schema_name = getenv('POSTGRES_DEMO_SCHEMA_NAME')

class ItemPostgresDAL(BasePostgresDAL):
    def __init__(self, pool_or_conn: Pool | Connection):
        super().__init__(pool_or_conn, table_name="items", schema_name=schema_name)
        self.schema_name = schema_name
        self.sql_functions = ItemSQLFunctions(schema=schema_name)

    async def get_by_name(self, name: str) -> bool:
        row = await self.execute_query("SELECT 1 FROM items WHERE name=$1", name)
        return row is not None
