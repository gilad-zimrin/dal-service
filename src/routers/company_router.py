from src.core.security import require_role, Role
from src.models.company import CompanyCreate, CompanyUpdate, CompanyRead
from src.routers.crud_router import CRUDRouter
from fastapi import Depends


class CompanyRouter(CRUDRouter):
    def __init__(self):
        super().__init__(prefix="/companies", tags=["companies"])
        self.register_routes(
            model_name='Company',
            model_create=CompanyCreate,
            model_update=CompanyUpdate,
            model_out=CompanyRead,
            dependencies=[Depends(require_role(Role.company))]
        )
