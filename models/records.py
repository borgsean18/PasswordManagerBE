from pydantic import BaseModel
from typing import Optional

class Record(BaseModel):
    name: str
    description: str
    username: str
    password: str
    is_weak: bool
    group_id: Optional[str] = None