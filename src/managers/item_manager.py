from .base_manager import BaseManager
from src.dal.item_dal import ItemPostgresDAL

class ItemManager(BaseManager):
    def __init__(self, dal: ItemPostgresDAL):
        super().__init__(dal)
