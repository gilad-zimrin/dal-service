from src.databases_access_layer.postgres_dal.functions_model.base_sql_functions import BaseSQLFunctions


class CompanySQLFunctions(BaseSQLFunctions):
    def __init__(self, schema):
        super().__init__(
            create_function="company_create",
            update_function="company_update",
            delete_function="company_delete",
            schema=schema,
        )
