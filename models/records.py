from pydantic import BaseModel
from typing import Optional

class Group(BaseModel):
    name: str
    icon: str


class Record(BaseModel):
    name: str
    description: str
    username: str
    password: str
    is_weak: bool
    group_id: Optional[str]