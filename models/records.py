from pydantic import BaseModel
from typing import Optional

class Folder(BaseModel):
    name: str
    icon: str
    color: str


class Record(BaseModel):
    name: str
    description: str
    username: str
    password: str
    folder_id: Optional[int]