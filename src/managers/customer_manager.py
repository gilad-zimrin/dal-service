from .base_manager import BaseManager
from src.databases_access_layer.postgres_dal.customer_dal import CustomerPostgresDAL

class CustomerManager(BaseManager):
    def __init__(self, dal: CustomerPostgresDAL):
        super().__init__(dal)

    @property
    def unique_field_name(self) -> str:
        return "customer_id"
