from typing import Any, TypeVar, Generic
from pydantic import BaseModel
from src.dal.base_postgres_dal import BasePostgresDAL

DALType = TypeVar("DALType", bound=BasePostgresDAL)


class BaseManager(Generic[DALType]):
    """
    BaseManager provides generic CRUD operations by delegating to a DAL.
    Each entity-specific manager should inherit from this class and can
    override or extend methods to implement domain-specific logic.
    """
    def __init__(self, dal: DALType):
        self.dal: DALType = dal

    async def create(self, data: dict[str, Any]) -> BaseModel:
        """
        Create a new entity using DAL.
        """
        return await self.dal.create(data)

    async def get(self, id_: Any) -> BaseModel | None:
        """
        Get a single entity by primary key.
        """
        return await self.dal.get(id_)

    async def get_all(self) -> list[BaseModel]:
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
