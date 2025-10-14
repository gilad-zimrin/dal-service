from src.databases_access_layer.postgres_dal.functions_model.base_sql_functions import BaseSQLFunctions


class OrderSQLFunctions(BaseSQLFunctions):
    def __init__(self, schema):
        super().__init__(
            create_function="order_create",
            update_function="order_update",
            delete_function="order_delete",
            schema=schema,
        )
