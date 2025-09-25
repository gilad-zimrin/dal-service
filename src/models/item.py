from datetime import datetime
from typing import Optional
from pydantic import BaseModel, StrictStr, StrictInt, StrictFloat


class Item(BaseModel):
    item_id: Optional[StrictInt]
    name: StrictStr
    description: Optional[StrictStr]
    price: StrictFloat
    created_at: datetime

    class Config:
        extra = "forbid"


class ItemCreate(Item):
    item_id: None = None
    name: StrictStr
    price: StrictFloat
    description: Optional[StrictStr]
    created_at: Optional[datetime] = None

class ItemUpdate(Item):
    item_id: None = None
    name: Optional[StrictStr] = None
    price: Optional[StrictFloat] = None
    description: Optional[StrictStr] = None
    created_at: Optional[datetime] = None

class ItemRead(Item):
    item_id: StrictInt
    name: StrictStr
    price: StrictFloat
    description: Optional[StrictStr]
    created_at: datetime
