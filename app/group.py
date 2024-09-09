from fastapi import APIRouter
from models.group import Group
group_router = APIRouter(prefix="/groups", tags=["Groups"])

@group_router.post("/create")
async def create_group(group: Group):
    pass