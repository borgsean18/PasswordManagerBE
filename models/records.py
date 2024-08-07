from pydantic import BaseModel
from typing import Optional

class Folder(BaseModel):
    name: str
    icon: str
    color: str


class Password(BaseModel):
    name: str
    description: str
    username: str
    password: str
    user_id: int
    folder_id: Optional[int]