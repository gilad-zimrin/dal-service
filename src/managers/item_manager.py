from .base_manager import BaseManager
from src.databases_access_layer.postgres_dal.item_dal import ItemPostgresDAL

class ItemManager(BaseManager):
    def __init__(self, dal: ItemPostgresDAL):
        super().__init__(dal)

    @property
    def unique_field_name(self) -> str:
        return "item_id"
