from typing import Optional

from pydantic import BaseModel, StrictInt, StrictStr

class Customers(BaseModel):
    customer_id: StrictInt
    username: StrictStr
    password: StrictStr
    email: StrictStr
    name: Optional[StrictStr] = None
    age: Optional[StrictInt] = None
    location: Optional[StrictStr] = None

# TODO add email verification

class CustomerCreate(Customers):
    customer_id: None = None

class CustomerUpdate(Customers):
    customer_id: None = None
    username: Optional[StrictStr] = None
    password: Optional[StrictStr] = None
    email: Optional[StrictStr] = None

class CustomerRead(Customers):
    pass
