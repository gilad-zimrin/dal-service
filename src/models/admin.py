import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, StrictInt, StrictStr, EmailStr, field_validator

from src.models.secure_base_model import SecureBaseModel


class Admin(BaseModel):
    admin_id: StrictInt
    username: StrictStr
    password: StrictStr
    email: EmailStr
    created_at: Optional[datetime]

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: StrictStr) -> StrictStr:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain an uppercase letter')
        return v

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

class AdminCreate(Admin):
    admin_id: None = None
    created_at: None = None

class AdminUpdate(Admin):
    admin_id: None = None
    username: Optional[StrictStr] = None
    password: Optional[StrictStr] = None
    email: Optional[StrictStr] = None
    created_at: None = None

    @field_validator('password')
    @classmethod
    def validate_password_update(cls, v: Optional[StrictStr]) -> Optional[StrictStr]:
        if v is not None:
            return cls.validate_password(v)  # Reuse base validation
        return v

class AdminRead(Admin, SecureBaseModel):
    created_at: datetime
