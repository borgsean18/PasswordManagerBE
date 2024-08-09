from fastapi import APIRouter, Header
from typing import Annotated
from app.validate import is_alphanumeric
from app.user import authenticate_user
from app.database import psql_create_record, psql_get_record, psql_delete_record, psql_search_user
from models.records import Record

password_router = APIRouter(prefix="/records", tags=["Records"])

@password_router.post("/create")
async def create_record(
    record: Record,
    auth_token: Annotated[str | None, Header(...)] = None,
    user_email: Annotated[str | None, Header(...)] = None
    ):
    try:
        await authenticate_user(auth_token=auth_token, user_email=user_email)

        user = await psql_search_user(user_email)

        # upload password to db
        await psql_create_record(record=record, user_id=user['id']) 

        return {"message":"success"}
    except Exception as e:
        return {"message": e}


@password_router.get("/")
async def get_record(
    record_name: str = None,
    auth_token: Annotated[str | None, Header(...)] = None,
    user_email: Annotated[str | None, Header(...)] = None,
    ):
    try:
        # Validate record_name
        if record_name is not None:
            is_alphanumeric(record_name)

        await authenticate_user(auth_token=auth_token, user_email=user_email)

        user = await psql_search_user(user_email)

        record = await psql_get_record(user['id'], record_name)

        return {
            "status":"200",
            "message": record
        }
    except Exception as e:
        return {
            "status":"400",
            "message": e
        }


@password_router.post("/update/{record_id}")
async def update_record(
    record: Record,
    record_id: int,
    auth_token: Annotated[str | None, Header(...)] = None,
    user_email: Annotated[str | None, Header(...)] = None
    ):
    try:
        await authenticate_user(auth_token=auth_token, user_email=user_email)

        # Update password in db if found
        # await psql_create_record(password=password)

        return {"message":"success"}
    except Exception as e:
        return {"message":e}


@password_router.get("/delete/{record_id}")
async def delete_record(
    record_id: int = None,
    auth_token: Annotated[str | None, Header(...)] = None,
    user_email: Annotated[str | None, Header(...)] = None,
    ):
    try:
        await authenticate_user(auth_token=auth_token, user_email=user_email)

        user_id = await psql_search_user(user_email)

        # Make sure it is not possible for user to delete record they dont own
        result = await psql_delete_record(record_id, user_id['id'])
    except Exception as e:
        return {
            "status": 500,
            "message": e.args
        }