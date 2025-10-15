from src.databases_access_layer.postgres_dal.functions_model.base_sql_functions import BaseSQLFunctions


class ItemSQLFunctions(BaseSQLFunctions):
    def __init__(self, schema):
        super().__init__(
            create_function="item_create",
            update_function="item_update",
            delete_function="item_delete",
            schema=schema,
        )
