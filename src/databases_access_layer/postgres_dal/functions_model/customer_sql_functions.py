from src.databases_access_layer.postgres_dal.functions_model.base_sql_functions import BaseSQLFunctions


class CustomerSQLFunctions(BaseSQLFunctions):
    def __init__(self, schema: str = "app"):
        super().__init__(
            create_function="customer_create",
            update_function="customer_update",
            delete_function="customer_delete",
            schema=schema,
        )
