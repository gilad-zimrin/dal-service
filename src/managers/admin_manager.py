from typing import Any

from .base_manager import BaseManager
from src.databases_access_layer.postgres_dal.admin_dal import AdminPostgresDAL
from ..core.exceptions.object_not_found_error import ObjectNotFoundError


class AdminManager(BaseManager):
    def __init__(self, dal: AdminPostgresDAL):
        super().__init__(dal)

    @property
    def unique_field_name(self) -> str:
        return "admin_id"

    async def get_by_username(self, username: str) -> dict | dict[str, Any] | None:
        try:
            return await self.dal.get_by_id(username, 'username')
        except ObjectNotFoundError:
            return None
