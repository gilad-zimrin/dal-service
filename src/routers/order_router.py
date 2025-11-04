from fastapi import Depends

from src.core.security import require_role, Role
from src.models.order import OrderCreate, OrderUpdate, OrderRead
from src.routers.crud_router import CRUDRouter


class OrderRouter(CRUDRouter):
    def __init__(self):
        super().__init__(prefix="/orders", tags=["orders"])
        self.register_routes(
            model_name='Order',
            model_create=OrderCreate,
            model_update=OrderUpdate,
            model_out=OrderRead,
            dependencies=[Depends(require_role(Role.company))]
        )

