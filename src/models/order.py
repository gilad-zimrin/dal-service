from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, StrictInt

from src.models.order_item import OrderItem, OrderItemCreate, OrderItemUpdate, OrderItemRead


class Order(BaseModel):
    order_id: StrictInt
    customer_id: StrictInt
    order_time: Optional[datetime]
    order_items: List[OrderItem]

class OrderCreate(Order):
    order_id: None = None
    order_time: None = None
    order_items: List[OrderItemCreate]


class OrderUpdate(Order):
    order_id: None = None
    customer_id: None = None
    order_time: None = None
    order_items: List[OrderItemUpdate] = []

class OrderRead(Order):
    order_time: datetime
    order_items: List[OrderItemRead]
