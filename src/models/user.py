from typing import List

from pydantic import BaseModel


class User(BaseModel):
    id: int | None = None
    name: str
    email: str


class UserCreate(BaseModel):
    name: str
    email: str

class ItemCreate(BaseModel):
    name: str
    description: str | None = None

class UserWithItems(BaseModel):
    user: UserCreate
    items: List[ItemCreate]
