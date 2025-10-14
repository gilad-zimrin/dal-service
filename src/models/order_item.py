from typing import Optional

from pydantic import BaseModel, StrictInt, StrictFloat, field_validator

class OrderItem(BaseModel):
    order_item_id: Optional[StrictInt]
    order_id: Optional[StrictInt]
    item_id: StrictInt
    quantity: StrictInt
    unit_price: StrictFloat

    @field_validator('quantity')
    @classmethod
    def quantity_must_be_positive(cls, v: StrictInt) -> StrictInt:
        if v <= 0:
            raise ValueError('quantity must be greater than 0')
        return v

class OrderItemCreate(OrderItem):
    order_item_id: None = None
    order_id: Optional[StrictInt] = None
    unit_price: None = None

class OrderItemUpdate(OrderItem):
    order_item_id: None = None
    order_id: Optional[StrictInt] = None
    item_id: Optional[StrictInt] = None
    quantity: Optional[StrictInt] = None
    unit_price: Optional[StrictFloat] = None

class OrderItemRead(OrderItem):
    order_item_id: StrictInt
    order_id: StrictInt
