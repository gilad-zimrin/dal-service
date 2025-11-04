from datetime import datetime
from typing import Optional

from pydantic import BaseModel, StrictInt, StrictStr, field_validator

from src.models.enums.industry import Industry
from src.models.secure_base_model import SecureBaseModel


class Company(BaseModel):
    company_id: StrictInt
    name: StrictStr
    username: StrictStr
    password: StrictStr
    email: StrictStr
    location: StrictStr
    industry: Industry
    employees: StrictInt
    register_time: Optional[datetime]

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: StrictStr) -> StrictStr:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain an uppercase letter')
        return v

class CompanyCreate(Company):
    company_id: None = None
    register_time: None = None

class CompanyUpdate(Company):
    company_id: None = None
    name: Optional[StrictStr] = None
    username: Optional[StrictStr] = None
    password: Optional[StrictStr] = None
    email: Optional[StrictStr] = None
    location: Optional[StrictStr] = None
    industry: Optional[Industry] = None
    employees: Optional[StrictInt] = None
    register_time: None = None

    @field_validator('password')
    @classmethod
    def validate_password_update(cls, v: Optional[StrictStr]) -> Optional[StrictStr]:
        if v is not None:
            return cls.validate_password(v)  # Reuse base validation
        return v

class CompanyRead(Company, SecureBaseModel):
    register_time: datetime

    class Config:
        fields = {'password': {'exclude': True}}
