from typing import Any, TypeVar, Generic
from pydantic import BaseModel

from src.dal.postgres_dal.base_postgres_dal import DALType


class BaseManager(Generic[DALType]):
    """
    BaseManager provides generic CRUD operations by delegating to a DAL.
    Each entity-specific manager should inherit from this class and can
    override or extend methods to implement domain-specific logic.
    """
    def __init__(self, dal: DALType):
        self.dal: DALType = dal
        self.unique_field_name = None

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Create a new entity using DAL.
        """
        return await self.dal.create(data)

    async def get(self, id_: Any) -> dict | dict[str, Any] | None:
        """
        Get a single entity by primary key.
        """
        if not self.unique_field_name:
            # TODO change into abstract property
            raise NotImplementedError("Unique field name not implemented on manager")
        return await self.dal.get_by_id(id_, self.unique_field_name)

    async def get_all(self) -> list[dict | dict[str, Any]]:
        """
        Get all entities.
        """
        return await self.dal.get_all()

    async def update(self, id_: Any, data: dict[str, Any]) -> BaseModel | None:
        """
        Update an entity by primary key.
        """
        return await self.dal.update(id_, data)

    async def delete(self, id_: Any) -> bool:
        """
        Delete an entity by primary key.
        """
        return await self.dal.delete(id_)
