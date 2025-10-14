from datetime import datetime
from typing import Optional
from pydantic import BaseModel, StrictStr, StrictInt, StrictFloat, field_validator


class Item(BaseModel):
    item_id: Optional[StrictInt]
    company_id: StrictInt
    name: StrictStr
    price: StrictFloat
    stock: StrictInt
    description: Optional[StrictStr]
    created_at: datetime

    class Config:
        extra = "forbid"

# TODO create a smaller version of these types, since that inherit, create a general convention for models
class ItemCreate(Item):
    item_id: None = None
    company_id: StrictInt
    name: StrictStr
    price: StrictFloat
    stock: StrictInt
    description: Optional[StrictStr]
    created_at: Optional[datetime] = None

    @field_validator('stock')
    @classmethod
    def stock_must_be_positive(cls, v: StrictInt) -> StrictInt:
        if v <= 0:
            raise ValueError('stock must be greater than 0')
        return v

    @field_validator('price')
    @classmethod
    def price_must_be_positive(cls, v: StrictInt) -> StrictInt:
        if v <= 0:
            raise ValueError('price must be greater than 0')
        return v

class ItemUpdate(Item):
    item_id: None = None
    company_id: Optional[StrictInt] = None
    name: Optional[StrictStr] = None
    price: Optional[StrictFloat] = None
    stock: Optional[StrictInt] = None
    description: Optional[StrictStr] = None
    created_at: Optional[datetime] = None

class ItemRead(Item):
    item_id: StrictInt
    company_id: StrictInt
    name: StrictStr
    price: StrictFloat
    stock: StrictInt
    description: Optional[StrictStr]
    created_at: datetime
