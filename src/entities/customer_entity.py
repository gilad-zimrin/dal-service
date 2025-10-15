from typing import Type

from src.databases_access_layer.postgres_dal.customer_dal import CustomerPostgresDAL
from src.entities.EntityConfig import EntityConfig, ModelT, DALT, ManagerT, RouterT
from src.managers import CustomerManager
from src.models.customer import Customer
from src.routers import CustomerRouter


class CustomerEntity(EntityConfig):
    @property
    def entity_name(self):
        return 'Customer'

    @property
    def entity_model(self) -> Type[ModelT]:
        return Customer

    @property
    def entity_dal(self) -> Type[DALT]:
        return CustomerPostgresDAL

    @property
    def entity_manager(self) -> Type[ManagerT]:
        return CustomerManager

    @property
    def entity_router(self) -> Type[RouterT]:
        return CustomerRouter

    def get_manager(self, connection) -> CustomerManager:
        return CustomerManager(self.get_dal(connection))

    def get_dal(self, connection) -> CustomerPostgresDAL:
        return CustomerPostgresDAL(connection)
