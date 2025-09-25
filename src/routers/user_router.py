from fastapi import HTTPException
from src.routers.crud_router import CRUDRouter
from src.managers.user_manager import UserManager
from src.databases_access_layer.postgres_dal.user_dal import UserPostgresDAL
from src.databases_access_layer.postgres_dal.item_dal import ItemPostgresDAL
from src.models.user import User, UserWithItems
from src.core.postgres_db_pool import postgres_connection_pool
from src.core.unit_of_work import UnitOfWork


class UserRouter(CRUDRouter):
    def __init__(self):
        super().__init__(prefix="/users", tags=["users"])

        # TODO update user modules
        self.register_routes(
            model_name='User',
            model_create=User,
            model_update=User,
            model_out=User
        )

        @self.post("/with-items")
        async def create_user_with_items(payload: UserWithItems):
            async with UnitOfWork(postgres_connection_pool, [UserPostgresDAL, ItemPostgresDAL]) as unit_of_work:
                user_manager = UserManager(
                    unit_of_work.UserPostgresDAL,
                    unit_of_work.ItemPostgresDAL
                )
                try:
                    result = await user_manager.create_user_with_items(payload.user, payload.items)
                    return result
                # TODO check if error handling is needed or middleware is enough
                except ValueError as e:
                    raise HTTPException(status_code=400, detail=str(e))
