from src.dal.postgres_dal.base_postgres_dal import BasePostgresDAL
from src.models.user import User
from asyncpg import Pool

class UserPostgresDAL(BasePostgresDAL):
    def __init__(self, pool_or_conn: Pool):
        super().__init__(pool_or_conn, table_name="users", model=User, schema_name='demo')
        # TODO maybe rename pool_or_conn

    async def exists_by_email(self, email: str) -> bool:
        row = await self._pool_or_conn.fetchrow("SELECT 1 FROM users WHERE email=$1", email)
        return row is not None
