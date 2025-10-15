import re
from typing import Optional

from pydantic import BaseModel, StrictInt, StrictStr, EmailStr, field_validator

class Customer(BaseModel):
    customer_id: StrictInt
    username: StrictStr
    password: StrictStr
    email: EmailStr
    name: Optional[StrictStr] = None
    age: Optional[StrictInt] = None
    location: Optional[StrictStr] = None

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
            raise ValueError('Invalid email format')

        forbidden_domains = ['mailinator.com', 'tempmail.com']
        domain = v.split('@')[1].lower()
        if domain in forbidden_domains:
            raise ValueError('Disposable email addresses are not allowed')
        return v

class CustomerCreate(Customer):
    customer_id: None = None

class CustomerUpdate(Customer):
    customer_id: None = None
    username: Optional[StrictStr] = None
    password: Optional[StrictStr] = None
    email: Optional[StrictStr] = None

class CustomerRead(Customer):
    pass
