from datetime import datetime
from typing import Optional

from pydantic import BaseModel, StrictInt, StrictStr

from src.models.enums.industry import Industry


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

class CompanyRead(Company):
    register_time: datetime