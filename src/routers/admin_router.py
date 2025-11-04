from fastapi import Depends

from src.core.security import Role, require_role
from src.models.admin import AdminCreate, AdminUpdate, AdminRead
from src.routers.crud_router import CRUDRouter


class AdminRouter(CRUDRouter):
    def __init__(self):
        super().__init__(prefix="/admins", tags=["admins"])
        self.register_routes(
            model_name='Admin',
            model_create=AdminCreate,
            model_update=AdminUpdate,
            model_out=AdminRead,
            dependencies=[Depends(require_role(Role.admin))]
        )
