from src.dal.postgres_dal.base_postgres_dal import BasePostgresDAL
from asyncpg import Pool, Connection

from src.dal.postgres_dal.sql_functions_model.item_sql_functions import ItemSQLFunctions
from src.models.user import ItemCreate

class ItemPostgresDAL(BasePostgresDAL):
    def __init__(self, pool_or_conn: Pool | Connection):
        super().__init__(pool_or_conn, table_name="items", model=ItemCreate)
        self.sql_functions = ItemSQLFunctions(schema="app")

    async def exists_by_name(self, name: str) -> bool:
        row = await self.pool.fetchrow("SELECT 1 FROM items WHERE name=$1", name)
        return row is not None
