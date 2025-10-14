from src.models.item import ItemCreate, ItemUpdate, ItemRead
from src.routers.crud_router import CRUDRouter


class ItemRouter(CRUDRouter):
    def __init__(self):
        super().__init__(prefix="/items", tags=["items"])
        self.register_routes(
            model_name='Item',
            model_create=ItemCreate,
            model_update=ItemUpdate,
            model_out=ItemRead
        )

# TODO add restock item route
