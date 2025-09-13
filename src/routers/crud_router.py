from typing import Callable, Any, Sequence

from fastapi import APIRouter, Depends
from pydantic import BaseModel


class CRUDRouter(APIRouter):
    """
    Base CRUDRouter for FastAPI.
    Inherit this class per entity and call register_routes()
    inside your __init__.
    """
    def register_routes(
        self,
        manager_factory: Callable[[], Any],
        model_in: type[BaseModel],
        model_out: type[BaseModel],
        include: Sequence[str] = ("create", "get", "list", "update", "delete"),
    ):
        """
        This function sets the default routes for each entity
        :param manager_factory: This factory if a function that returns a manager object for the
        model, calling it in fastAPI's Defends function to we make sure a new manager is created every
        time, since the manager might not be stateless.
        :param model_in: The type enforced in the request
        :param model_out: The type enforced in the response
        :param include: Specify the route you want to include, if you don't want all
        :return:
        """

        if "create" in include:
            @self.post("/", response_model=model_out)
            async def create_item(data: model_in, manager=Depends(manager_factory)):
                return await manager.create(data.model_dump())

        if "get" in include:
            @self.get("/{id_}", response_model=model_out)
            async def get_item(id_: int, manager=Depends(manager_factory)):
                return await manager.get(id_)

        if "list" in include:
            @self.get("/", response_model=list[model_out])
            async def list_items(manager=Depends(manager_factory)):
                return await manager.get_all()

        if "update" in include:
            @self.put("/{id_}", response_model=model_out)
            async def update_item(id_: int, data: model_in, manager=Depends(manager_factory)):
                return await manager.update(id_, data.model_dump())

        if "delete" in include:
            @self.delete("/{id_}")
            async def delete_item(id_: int, manager=Depends(manager_factory)):
                success = await manager.delete(id_)
                return {"deleted": success}
