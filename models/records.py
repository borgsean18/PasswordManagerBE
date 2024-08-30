from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class Group(BaseModel):
    name: str
    icon: str


class Record(BaseModel):
    id: Optional[UUID] = None
    name: str
    description: str
    username: str
    password: str
    is_weak: bool
    group_id: Optional[str] = None