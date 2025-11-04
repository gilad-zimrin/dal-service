from typing import Sequence

from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel

from src.managers.base_manager import BaseManager


class CRUDRouter(APIRouter):
    def register_routes(
        self,
        model_name: str,
        model_create: type[BaseModel],
        model_update: type[BaseModel],
        model_out: type[BaseModel],
        dependencies=None,
        include: Sequence[str] = ("create", "get", "list", "update", "delete"),
    ):
        """
        Base CRUDRouter for FastAPI.
        Inherit this class per entity and call register_routes()
        inside your __init__.
        This function sets the default routes for each entity
        :param model_name: The model name, as written in function set_app_managers in app_config
        :param model_create: The type enforced in the create request
        :param model_update: The type enforced in the update request
        :param model_out: The type enforced in the response
        :param dependencies: A list of optional dependencies
        :param include: Specify the route you want to include, if you don't want all
        :return:
        """

        if dependencies is None:
            dependencies = []

        def get_manager(request: Request) -> BaseManager:
            return request.app.state.postgres_managers[model_name]

        if "create" in include:
            @self.post("/", response_model=model_out, dependencies=dependencies)
            async def create_object(data: model_create, manager: BaseManager = Depends(get_manager)):
                return await manager.create(data.model_dump())

        if "get" in include:
            @self.get("/{id_}", response_model=model_out, dependencies=dependencies)
            async def get_object(id_: int, manager: BaseManager = Depends(get_manager)):
                return await manager.get(id_)

        if "list" in include:
            @self.get("/", response_model=list[model_out], dependencies=dependencies)
            async def list_objects(manager: BaseManager = Depends(get_manager)):
                return await manager.get_all()

        if "update" in include:
            @self.put("/{id_}", response_model=model_out, dependencies=dependencies)
            async def update_object(id_: int, data: model_update, manager: BaseManager = Depends(get_manager)):
                return await manager.update(id_, data.model_dump())

        if "delete" in include:
            @self.delete("/{id_}", dependencies=dependencies)
            async def delete_object(id_: int, manager: BaseManager = Depends(get_manager)):
                success = await manager.delete(id_)
                return {"deleted": success}
