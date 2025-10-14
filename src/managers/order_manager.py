import json
from datetime import datetime
from typing import Any

from src.databases_access_layer.postgres_dal.order_dal import OrderPostgresDAL
from . import ItemManager
from .base_manager import BaseManager
from ..core.exceptions.stock_error import StockError
from ..models.order_item import OrderItemUpdate, OrderItemCreate, OrderItemRead


class OrderManager(BaseManager):
    def __init__(self, dal: OrderPostgresDAL, item_manager: ItemManager):
        super().__init__(dal)
        self.item_manager: ItemManager = item_manager

    @property
    def unique_field_name(self) -> str:
        return "order_id"

    async def create(self, new_object: dict[str, Any]) -> dict[str, Any]:
        """
        This function handles creating a new order.
        It fills automatically-filled fields (like order_time and order_items.unit_price), while also checking that
        there are enough items in stock.
        this function does not decrement the ordered items from the stock, the sql function does that.
        :param new_object: The new create_order request
        :return: the new order created
        """
        new_object['order_time'] = datetime.now()

        [await self.allocate_new_order(item) for item in new_object['order_items']]

        return json.loads((await self.dal.create(new_object))['order_create'])

    async def get(self, id_: Any) -> dict | dict[str, Any] | None:
        """
        Parse the items returned as JSONB using asyncpg
        """
        if not self.unique_field_name:
            raise NotImplementedError("Unique field name not implemented on manager")
        order = await self.dal.get_by_id(id_, self.unique_field_name)
        order['order_items'] = json.loads(order['order_items'])
        return order

    async def get_all(self) -> list[dict | dict[str, Any]]:
        rows = await self.dal.get_all()
        return [
            {
                "order_id": row["order_id"],
                "customer_id": row["customer_id"],
                "order_time": row["order_time"].isoformat() if row["order_time"] else None,
                "order_items": json.loads(row["order_items"]) if row["order_items"] else []
                # TODO have asyncpg parse it automatically without using json.loads
            }
            for row in rows
        ]

    async def update(self, id_: Any, updated_object: dict[str, Any]) -> dict[str, Any] | None:
        old_order_items = json.loads((await self.dal.get_by_id(id_, self.unique_field_name))['order_items'])

        old_order_items_ids = {item["item_id"]: item for item in old_order_items}
        for current_item in updated_object['order_items']:
            canceled_quantity = 0
            if old_order_items_ids.get(current_item['item_id']):
                canceled_quantity = old_order_items_ids[current_item['item_id']]['quantity']

            await self.allocate_new_order(current_item, canceled_quantity)

        return json.loads((await self.dal.update(id_, updated_object))['order_update'])

    async def delete(self, id_: Any) -> bool:
        return await self.dal.delete(id_)


    async def allocate_new_order(
            self, item: OrderItemCreate | OrderItemUpdate, canceled_quantity: int = 0
    ) -> OrderItemCreate | OrderItemUpdate:
        """
        For an item in an order, this function fills automatically-filled fields
        (like order_time and order_items.unit_price), and also checking that there are enough items in stock.
        :param item: The item that the function handles
        :param canceled_quantity: If an order was updated, that's the amount ordered from the old order
        :return:
        """
        existing_item = await self.item_manager.get(item['item_id'])
        if existing_item['stock'] + canceled_quantity < item['quantity']:
            raise StockError(f'Not enough items in stock for item_id {item['item_id']}')
        if item['quantity'] == 0:
            raise ValueError("Can not order 0 quantity of an item")
        item['unit_price'] = existing_item['price']
        return item


