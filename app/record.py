from fastapi import APIRouter, Header
from typing import Annotated
from app.user import authenticate_user
from app.database import psql_create_record, psql_get_record
from models.records.models import Password

password_router = APIRouter(prefix="/records", tags=["Records"])

@password_router.post("/create")
async def create_record(
    password: Password,
    auth_token: Annotated[str | None, Header(...)] = None,
    user_email: Annotated[str | None, Header(...)] = None
    ):
    try:
        await authenticate_user(auth_token=auth_token, user_email=user_email)

        # upload password to db
        await psql_create_record(password=password) 

        return {"message":"success"}
    except Exception as e:
        return {"message": e}


@password_router.get("/get")
async def get_record(
    record_name:str = None,
    auth_token: Annotated[str | None, Header(...)] = None,
    user_email: Annotated[str | None, Header(...)] = None,
    ):
    try:
        await authenticate_user(auth_token=auth_token, user_email=user_email)

        record = await psql_get_record(user_email, record_name)

        return {
            "status":"200",
            "message": record
        }
    except Exception as e:
        return {"message":f"Exception: {e}"}


@password_router.post("/update")
async def update_record(
    password: Password,
    auth_token: Annotated[str | None, Header(...)] = None,
    user_email: Annotated[str | None, Header(...)] = None
    ):
    try:
        await authenticate_user(auth_token=auth_token, user_email=user_email)

        # Update password in db if found
        await psql_create_record(password=password)

        return {"message":"success"}
    except Exception as e:
        return {"message":e}


@password_router.get("/delete")
async def delete_record(
    id: int
    ):
    return id