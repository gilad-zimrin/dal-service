from typing import Type

from src.databases_access_layer.postgres_dal.company_dal import CompanyPostgresDAL
from src.entities.EntityConfig import EntityConfig, ModelT, DALT, ManagerT, RouterT
from src.managers import CompanyManager
from src.models.company import Company
from src.routers import CompanyRouter


class CompanyEntity(EntityConfig):
    @property
    def entity_name(self):
        return 'Company'

    @property
    def entity_model(self) -> Type[ModelT]:
        return Company

    @property
    def entity_dal(self) -> Type[DALT]:
        return CompanyPostgresDAL

    @property
    def entity_manager(self) -> Type[ManagerT]:
        return CompanyManager

    @property
    def entity_router(self) -> Type[RouterT]:
        return CompanyRouter

    def get_manager(self, connection) -> CompanyManager:
        return CompanyManager(self.get_dal(connection))

    def get_dal(self, connection) -> CompanyPostgresDAL:
        return CompanyPostgresDAL(connection)
