from typing import Any

from .base_manager import BaseManager
from src.databases_access_layer.postgres_dal.customer_dal import CustomerPostgresDAL
from ..core.exceptions.object_not_found_error import ObjectNotFoundError


class CustomerManager(BaseManager):
    def __init__(self, dal: CustomerPostgresDAL):
        super().__init__(dal)

    @property
    def unique_field_name(self) -> str:
        return "customer_id"

    async def get_by_username(self, username: str) -> dict | dict[str, Any] | None:
        try:
            return await self.dal.get_by_id(username, 'username')
        except ObjectNotFoundError:
            return None
