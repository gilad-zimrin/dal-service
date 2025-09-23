from src.core.exceptions.configuration_error import ConfigurationError
from src.managers.base_manager import BaseManager
from src.dal.postgres_dal.user_dal import UserPostgresDAL
from src.dal.postgres_dal.item_dal import ItemPostgresDAL
from src.models.user import UserCreate, ItemCreate

class UserManager(BaseManager[UserPostgresDAL]):
    def __init__(self, user_dal: UserPostgresDAL, item_dal: ItemPostgresDAL = None):
        super().__init__(user_dal)
        self.item_dal = item_dal

    async def create_user_with_items(self, user: UserCreate, items: list[ItemCreate]):
        if not self.item_dal:
            raise ConfigurationError("User manager doesn't have item_dal configured")

        if await self.dal.exists_by_email(user.email):
            raise ValueError("User already exists")

        created_user = await self.dal.create(user.model_dump())

        created_items = []
        for item in items:
            if not await self.item_dal.exists_by_name(item.name):
                created_items.append(await self.item_dal.create(item.model_dump()))

        return {
            "user": created_user,
            "new_items": created_items
        }
