from abc import ABC, abstractmethod, abstractproperty
from typing import Type, Generic, TypeVar
from pydantic import BaseModel
from fastapi import APIRouter

from src.databases_access_layer.postgres_dal.base_postgres_dal import BasePostgresDAL
from src.managers.base_manager import BaseManager

ModelT = TypeVar("ModelT", bound=BaseModel)
RouterT = TypeVar("RouterT", bound=APIRouter)
ManagerT = TypeVar("ManagerT", bound=BaseManager)
DALT = TypeVar("DALT", bound=BasePostgresDAL)

class EntityConfig(ABC, Generic[ModelT, RouterT, ManagerT, DALT]):
    """Abstract base class enforcing structure for all entity configurations.

    When creating a new entity, one must create an entity config subclass.
    Attributes are enforced in order to keep the code's structure

    * Each entity subclass must be added to the list all_entities in app_config to connect it to the app *

    Subclasses must define the following abstract attributes:
    - entity_name: A string identifier for the entity.
    - entity_model: The Pydantic model class for the entity.
    - entity_router: The FastAPI router class for the entity.
    - entity_manager: The manager class for handling entity logic.
    - entity_dal: The data access layer class for database operations.
    """

    @property
    @abstractmethod
    def entity_name(self) -> str:
        """The name of the entity (e.g., 'user', 'product')."""
        pass

    @property
    @abstractmethod
    def entity_model(self) -> Type[ModelT]:
        """The Pydantic model class for the entity."""
        pass

    @property
    @abstractmethod
    def entity_router(self) -> Type[RouterT]:
        """The FastAPI router class for handling entity routes."""
        pass

    @property
    @abstractmethod
    def entity_manager(self) -> Type[ManagerT]:
        """The manager class for handling entity business logic."""
        pass

    @property
    @abstractmethod
    def entity_dal(self) -> Type[DALT]:
        """The data access layer class for database operations."""
        pass

    @abstractmethod
    def get_manager(self, connection) -> ManagerT:
        """Return a new manager instance for this entity."""
        pass

    @abstractmethod
    def get_dal(self, connection) -> DALT:
        """Return a new DAL instance for this entity."""
        pass