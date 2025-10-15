from typing import Type

from src.databases_access_layer.postgres_dal.item_dal import ItemPostgresDAL
from src.entities.EntityConfig import EntityConfig, ModelT, DALT, ManagerT, RouterT
from src.managers import ItemManager
from src.models.item import Item
from src.routers import ItemRouter


class ItemEntity(EntityConfig):
    @property
    def entity_name(self):
        return 'Item'

    @property
    def entity_model(self) -> Type[ModelT]:
        return Item

    @property
    def entity_dal(self) -> Type[DALT]:
        return ItemPostgresDAL

    @property
    def entity_manager(self) -> Type[ManagerT]:
        return ItemManager

    @property
    def entity_router(self) -> Type[RouterT]:
        return ItemRouter

    def get_manager(self, connection) -> ItemManager:
        return ItemManager(self.get_dal(connection))

    def get_dal(self, connection) -> ItemPostgresDAL:
        return ItemPostgresDAL(connection)
