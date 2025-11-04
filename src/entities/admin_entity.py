from typing import Type

from src.databases_access_layer.postgres_dal.admin_dal import AdminPostgresDAL
from src.entities.EntityConfig import EntityConfig, ModelT, DALT, ManagerT, RouterT
from src.managers import AdminManager
from src.models.admin import Admin
from src.routers import AdminRouter


class AdminEntity(EntityConfig):
    @property
    def entity_name(self):
        return 'Admin'

    @property
    def entity_model(self) -> Type[ModelT]:
        return Admin

    @property
    def entity_dal(self) -> Type[DALT]:
        return AdminPostgresDAL

    @property
    def entity_manager(self) -> Type[ManagerT]:
        return AdminManager

    @property
    def entity_router(self) -> Type[RouterT]:
        return AdminRouter

    def get_manager(self, connection) -> AdminManager:
        return AdminManager(self.get_dal(connection))

    def get_dal(self, connection) -> AdminPostgresDAL:
        return AdminPostgresDAL(connection)
