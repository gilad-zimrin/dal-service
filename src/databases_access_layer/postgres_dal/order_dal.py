import asyncio
from os import getenv

from asyncpg import Pool, Connection

from src.databases_access_layer.postgres_dal.base_postgres_dal import BasePostgresDAL
from src.databases_access_layer.postgres_dal.functions_model.order_sql_functions import OrderSQLFunctions

schema_name = getenv('POSTGRES_DEMO_SCHEMA_NAME')

class OrderPostgresDAL(BasePostgresDAL):
    def __init__(self, pool_or_conn: Pool | Connection):
        super().__init__(pool_or_conn, table_name="orders", schema_name=schema_name)
        self.schema_name = schema_name
        self.sql_functions = OrderSQLFunctions(schema=schema_name)
        self.get_by_id_query = """
        SELECT
            demo.orders.order_id,
            demo.orders.customer_id,
            demo.orders.order_time,
            jsonb_agg(
                jsonb_build_object(
                    'order_id', demo.order_items.order_id,
                    'order_item_id', demo.order_items.order_item_id,
                    'item_id', demo.order_items.item_id,
                    'quantity', demo.order_items.quantity,
                    'unit_price', demo.order_items.unit_price
                )
            ) FILTER (WHERE demo.order_items.order_item_id IS NOT NULL) AS order_items
        FROM demo.orders
        LEFT JOIN demo.order_items
            ON demo.orders.order_id = demo.order_items.order_id
        WHERE demo.orders.order_id = $object_id
        GROUP BY demo.orders.order_id, demo.orders.customer_id, demo.orders.order_time;
        """
        self.get_all_query = """
                SELECT
                    demo.orders.order_id,
                    demo.orders.customer_id,
                    demo.orders.order_time,
                    jsonb_agg(
                        jsonb_build_object(
                            'order_id', demo.order_items.order_id,
                            'order_item_id', demo.order_items.order_item_id,
                            'item_id', demo.order_items.item_id,
                            'quantity', demo.order_items.quantity,
                            'unit_price', demo.order_items.unit_price
                        )
                    ) FILTER (WHERE demo.order_items.order_item_id IS NOT NULL) AS order_items
                FROM demo.orders
                LEFT JOIN demo.order_items
                    ON demo.orders.order_id = demo.order_items.order_id
                GROUP BY demo.orders.order_id, demo.orders.customer_id, demo.orders.order_time;
                """
