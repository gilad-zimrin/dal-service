from asyncpg import Pool

class UnitOfWork:
    """
    Generic UnitOfWork for asyncpg.
    Usage:
        async with UnitOfWork(pool, [UserPostgresDAL, ItemPostgresDAL]) as uow:
            await uow.UserPostgresDAL.create(...)
            await uow.ItemPostgresDAL.create(...)

    This Unit of work will hold a single connection though multiple queries to create a single transaction
    """
    def __init__(self, pool: Pool, dal_classes: list[type]):
        self.pool = pool
        self.dal_classes = dal_classes
        self.dal_list = {}

    async def __aenter__(self):
        # acquire one connection and start a transaction
        self.conn = await self.pool.acquire()
        self.tx = self.conn.transaction()
        await self.tx.__aenter__()

        # instantiate each DAL bound to this connection
        for dal_class in self.dal_classes:
            name = dal_class.__name__
            self.dal_list[name] = dal_class(self.conn)

        return self  # to access uow.dal_list['UserPostgresDAL'] etc.

    async def __aexit__(self, exc_type, exc, tb):
        await self.tx.__aexit__(exc_type, exc, tb)
        await self.pool.release(self.conn)

    def __getattr__(self, item):
        """Allow UnitOfWork.UserPostgresDAL or UnitOfWork.UserPostgresDAL to access the DAL directly."""
        if item in self.dal_list:
            return self.dal_list[item]
        raise AttributeError(f"No DAL named {item}")
