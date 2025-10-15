from os import getenv

from asyncpg import Pool, Connection
from src.databases_access_layer.postgres_dal.functions_model.customer_sql_functions import CustomerSQLFunctions

from src.databases_access_layer.postgres_dal.base_postgres_dal import BasePostgresDAL

schema_name = getenv('POSTGRES_DEMO_SCHEMA_NAME')

class CustomerPostgresDAL(BasePostgresDAL):
    def __init__(self, pool_or_conn: Pool | Connection):
        super().__init__(pool_or_conn, table_name="customers", schema_name=schema_name)
        self.schema_name = schema_name
        self.sql_functions = CustomerSQLFunctions(schema=schema_name)
