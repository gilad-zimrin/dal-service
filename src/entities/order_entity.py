from typing import Type

from src.databases_access_layer.postgres_dal.item_dal import ItemPostgresDAL
from src.databases_access_layer.postgres_dal.order_dal import OrderPostgresDAL
from src.entities.EntityConfig import EntityConfig, ModelT, DALT, ManagerT, RouterT
from src.managers import OrderManager, ItemManager
from src.models.order import Order
from src.routers import OrderRouter


class OrderEntity(EntityConfig):
    @property
    def entity_name(self):
        return 'Order'

    @property
    def entity_model(self) -> Type[ModelT]:
        return Order

    @property
    def entity_dal(self) -> Type[DALT]:
        return OrderPostgresDAL

    @property
    def entity_manager(self) -> Type[ManagerT]:
        return OrderManager

    @property
    def entity_router(self) -> Type[RouterT]:
        return OrderRouter

    def get_manager(self, connection) -> OrderManager:
        return OrderManager(self.get_dal(connection), ItemManager(ItemPostgresDAL(connection)))

    def get_dal(self, connection) -> OrderPostgresDAL:
        return OrderPostgresDAL(connection)
