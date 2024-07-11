from fastapi import APIRouter
from models import Password

password_router = APIRouter(prefix="/password")

@password_router.post("/create")
async def create_password(password: Password):
    pass