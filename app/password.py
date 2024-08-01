from fastapi import APIRouter, Header
from typing import Annotated
from app.user import authenticate_user
from app.database import psql_create_record
from models.records.models import Password

password_router = APIRouter(prefix="/records", tags=["Records"])

@password_router.post("/CreateRecord")
async def create_record(
    password: Password,
    auth_token: Annotated[str | None, Header(...)] = None,
    user_email: Annotated[str | None, Header(...)] = None
    ):
    try:
        auth = await authenticate_user(auth_token=auth_token, user_email=user_email)

        # upload password to db
        result = await psql_create_record(password=password) 

        return {"message":"success"}
    except Exception as e:
        return {"message": e}


@password_router.get("/GetRecord/")
async def get_record(
    id: int
    ):
    return id


@password_router.post("/UpdateRecord/")
async def update_record(
    password: Password,
    auth_token: Annotated[str | None, Header(...)] = None,
    user_email: Annotated[str | None, Header(...)] = None
    ):
    try:
        auth = await authenticate_user(auth_token=auth_token, user_email=user_email)

        # Update password in db if found
        result = await psql_create_record(password=password)

        return {"message":"success"}
    except Exception as e:
        return {"message":e}


@password_router.get("/DeleteRecord/")
async def delete_record(
    id: int
    ):
    return id