from src.core.postgres_db_pool import get_postgres_pool
from src.dal.postgres_dal.item_dal import ItemPostgresDAL
from src.managers.item_manager import ItemManager
from src.models.item import ItemCreate, ItemUpdate, ItemRead
from src.routers.crud_router import CRUDRouter
from asyncpg.pool import Pool
from fastapi import Depends


def item_manager_factory(postgres_connection_pool: Pool = Depends(get_postgres_pool)):
    return ItemManager(ItemPostgresDAL(postgres_connection_pool))

class ItemRouter(CRUDRouter):
    def __init__(self):
        super().__init__(prefix="/items", tags=["items"])
        self.register_routes(
            manager_factory=item_manager_factory,
            model_create=ItemCreate,
            model_update=ItemUpdate,
            model_out=ItemRead
        )

