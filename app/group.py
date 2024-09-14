from fastapi import APIRouter
from models.group import Group

group_router = APIRouter(prefix="/groups", tags=["Groups"])

@group_router.post("/create")
async def create_group(group: Group):
    pass

@group_router.get("/")
async def get_all_groups():
    pass

@group_router.get("/{group_id}")
async def get_group(group_id: str):
    pass

@group_router.put("/{group_id}")
async def update_group(group_id: str, group: Group):
    pass

@group_router.delete("/{group_id}")
async def delete_group(group_id: str):
    pass