from typing import Callable, Any, Sequence

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.models.create_response import CreateResponse


class CRUDRouter(APIRouter):
    """
    Base CRUDRouter for FastAPI.
    Inherit this class per entity and call register_routes()
    inside your __init__.
    """
    def register_routes(
        self,
        manager_factory: Callable[[], Any],
        model_create: type[BaseModel],
        model_update: type[BaseModel],
        model_out: type[BaseModel],
        include: Sequence[str] = ("create", "get", "list", "update", "delete"),
    ):
        """
        This function sets the default routes for each entity
        :param manager_factory: This factory if a function that returns a manager object for the
        model, calling it in fastAPI's Defends function to we make sure a new manager is created every
        time, since the manager might not be stateless.
        :param model_create: The type enforced in the create request
        :param model_update: The type enforced in the update request
        :param model_out: The type enforced in the response
        :param include: Specify the route you want to include, if you don't want all
        :return:
        """
        # TODO in the crud router, no need to Depend on a new manager
        if "create" in include:
            @self.post("/", response_model=CreateResponse)
            async def create_object(data: model_create, manager=Depends(manager_factory)):
                response = await manager.create(data.model_dump())
                return CreateResponse(**response)

        if "get" in include:
            @self.get("/{id_}", response_model=model_out)
            async def get_object(id_: int, manager=Depends(manager_factory)):
                return await manager.get(id_)

        if "list" in include:
            @self.get("/", response_model=list[model_out])
            async def list_objects(manager=Depends(manager_factory)):
                return await manager.get_all()

        if "update" in include:
            @self.put("/{id_}", response_model=model_out)
            async def update_object(id_: int, data: model_update, manager=Depends(manager_factory)):
                return await manager.update(id_, data.model_dump())

        if "delete" in include:
            @self.delete("/{id_}")
            async def delete_object(id_: int, manager=Depends(manager_factory)):
                success = await manager.delete(id_)
                return {"deleted": success}
