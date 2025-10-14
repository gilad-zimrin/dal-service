from .base_manager import BaseManager
from src.databases_access_layer.postgres_dal.company_dal import CompanyPostgresDAL

class CompanyManager(BaseManager):
    def __init__(self, dal: CompanyPostgresDAL):
        super().__init__(dal)

    @property
    def unique_field_name(self) -> str:
        return "company_id"
