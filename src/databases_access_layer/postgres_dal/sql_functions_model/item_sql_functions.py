from src.databases_access_layer.postgres_dal.sql_functions_model.base_sql_functions import BaseSQLFunctions


class ItemSQLFunctions(BaseSQLFunctions):
    def __init__(self, schema: str = "app"):
        # these names must match the functions you install via Alembic
        super().__init__(
            create_function="item_create",
            update_function="item_update",
            delete_function="item_delete",
            schema=schema,
        )
