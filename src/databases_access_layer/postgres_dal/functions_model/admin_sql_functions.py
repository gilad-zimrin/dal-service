from src.databases_access_layer.postgres_dal.functions_model.base_sql_functions import BaseSQLFunctions


class AdminSQLFunctions(BaseSQLFunctions):
    def __init__(self, schema: str = "app"):
        super().__init__(
            create_function="admin_create",
            update_function="admin_update",
            delete_function="admin_delete",
            schema=schema,
        )
