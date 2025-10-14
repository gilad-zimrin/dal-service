from src.models.customer import CustomerCreate, CustomerUpdate, CustomerRead
from src.routers.crud_router import CRUDRouter


class CustomerRouter(CRUDRouter):
    def __init__(self):
        super().__init__(prefix="/customers", tags=["customers"])
        self.register_routes(
            model_name='Customer',
            model_create=CustomerCreate,
            model_update=CustomerUpdate,
            model_out=CustomerRead
        )
