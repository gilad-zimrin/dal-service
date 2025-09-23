from src.routers.crud_router import CRUDRouter
from src.managers.item_manager import ItemManager
from src.dal.postgres_dal.item_dal import ItemPostgresDAL
from src.models.item import Item
from src.core.postgres_db_pool import pool

def item_manager_factory():
    return ItemManager(ItemPostgresDAL(pool))

class ItemRouter(CRUDRouter):
    def __init__(self):
        super().__init__(prefix="/items", tags=["items"])
        self.register_routes(
            manager_factory=item_manager_factory,
            model_in=Item,
            model_out=Item
        )
