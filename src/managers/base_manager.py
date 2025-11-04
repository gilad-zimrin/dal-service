from abc import abstractmethod, ABC
from typing import Any, Generic

from pydantic import BaseModel

from src.core.security import get_password_hash
from src.databases_access_layer.postgres_dal.base_postgres_dal import DALType


class BaseManager(Generic[DALType], ABC):
    """
    BaseManager provides generic CRUD operations by delegating to a DAL.
    Each entity-specific manager should inherit from this class and can
    override or extend methods to implement domain-specific logic.
    """
    def __init__(self, dal: DALType):
        self.dal: DALType = dal

    @property
    @abstractmethod
    def unique_field_name(self) -> str:
        """The unique column for this object, will be used at 'get_by_id'"""
        pass

    async def create(self, new_object: dict[str, Any]) -> dict[str, Any]:
        """
        Create a new entity using DAL.
        """
        if 'password' in new_object:
            new_object['password'] = get_password_hash(new_object['password'])
        return await self.dal.create(new_object)

    async def get(self, id_: Any) -> dict | dict[str, Any] | None:
        """
        Get a single entity by primary key.
        """
        if not self.unique_field_name:
            raise NotImplementedError("Unique field name not implemented on manager")
        return await self.dal.get_by_id(id_, self.unique_field_name)

    async def get_all(self) -> list[dict | dict[str, Any]]:
        """
        Get all entities.
        """
        return await self.dal.get_all()


    async def update(self, id_: Any, updated_object: dict[str, Any]) -> BaseModel | None:
        """
        Update an entity by primary key.
        """
        if updated_object.get('password'):
            updated_object['password'] = get_password_hash(updated_object['password'])
        return await self.dal.update(id_, updated_object)

    async def delete(self, id_: Any) -> bool:
        """
        Delete an entity by primary key.
        """
        return await self.dal.delete(id_)
