from fastapi import APIRouter, Header
from typing import Annotated
from app.validate import is_alphanumeric
from app.user import authenticate_user
from app.database import psql_create_record, psql_get_record, psql_delete_record, psql_search_user, psql_update_record
from models.records import Record

record_router = APIRouter(prefix="/records", tags=["Records"])

@record_router.post("/create")
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
        return {"message": e.args}

@record_router.get("/{user_id}")
async def get_all_records(
    user_id:int,
    auth_token: Annotated[str | None, Header(...)] = None,
    user_email: Annotated[str | None, Header(...)] = None,
    ):
    try:
        await authenticate_user(auth_token=auth_token, user_email=user_email)

        user = await psql_search_user(user_email)

        

    except Exception as e:
        return {
            "status": 400,
            "message": e
        }

@record_router.get("/{record_name}")
async def get_record(
    record_name: str,
    auth_token: Annotated[str | None, Header(...)] = None,
    user_email: Annotated[str | None, Header(...)] = None,
    ):
    try:
        # Validate record_name
        if record_name is not None:
            is_alphanumeric(record_name)

        await authenticate_user(auth_token=auth_token, user_email=user_email)

        user = await psql_search_user(user_email)

        record = await psql_get_record(user_id=user['id'], record_name=record_name)

        return {
            "status":"200",
            "message": record
        }
    except Exception as e:
        return {
            "status":"400",
            "message": e
        }


@record_router.post("/update/{record_id}")
async def update_record(
    record_id: int,
    record_data: Record,
    auth_token: Annotated[str | None, Header(...)] = None,
    user_email: Annotated[str | None, Header(...)] = None
    ):
    try:
        await authenticate_user(auth_token=auth_token, user_email=user_email)

        user = await psql_search_user(user_email)

        record = await psql_get_record(user_id=user['id'], record_id=record_id)

        response = await psql_update_record(record_id=record_id, user_id=user['id'], record_data=record_data)

        return response
    except Exception as e:
        return {
            "status": 400,
            "message":e.args
        }


@record_router.get("/delete/{record_id}")
async def delete_record(
    record_id: int = None,
    auth_token: Annotated[str | None, Header(...)] = None,
    user_email: Annotated[str | None, Header(...)] = None,
    ):
    try:
        await authenticate_user(auth_token=auth_token, user_email=user_email)

        user = await psql_search_user(user_email)

        # Make sure it is not possible for user to delete record they dont own
        await psql_delete_record(record_id, user['id'])

        return {
            "status": 200,
            "message": "Deleted Record Successfully"
        }
    except Exception as e:
        return {
            "status": 500,
            "message": e.args
        }