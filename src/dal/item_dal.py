from src.dal.base_postgres_dal import BasePostgresDAL
from asyncpg import Pool, Connection
from src.models.user import ItemCreate

class ItemPostgresDAL(BasePostgresDAL):
    def __init__(self, pool_or_conn: Pool | Connection):
        super().__init__(pool_or_conn, table_name="items", model=ItemCreate)

    async def exists_by_name(self, name: str) -> bool:
        row = await self.pool.fetchrow("SELECT 1 FROM items WHERE name=$1", name)
        return row is not None
