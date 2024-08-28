from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.database import psql_create_record, psql_get_record, psql_delete_record, psql_update_record
from models.records import Record

record_router = APIRouter(prefix="/records", tags=["Records"])

@record_router.post("/create")
async def create_record(
    record: Record,
    user: dict = Depends(get_current_user)
):
    try:
        await psql_create_record(record=record, user_id=user['id'])
        return {"message": "success"}
    except Exception as e:
        return {"message": str(e)}

@record_router.get("/{record_name}")
async def get_record(
    record_name: str,
    user: dict = Depends(get_current_user)
):
    try:
        record = await psql_get_record(user_id=user['id'], record_name=record_name)
        return {"status": "200", "message": record}
    except Exception as e:
        return {"status": "400", "message": str(e)}

@record_router.post("/update/{record_id}")
async def update_record(
    record_id: int,
    record_data: Record,
    user: dict = Depends(get_current_user)
):
    try:
        await psql_get_record(user_id=user['id'], record_id=record_id)
        response = await psql_update_record(record_id=record_id, user_id=user['id'], record_data=record_data)
        return response
    except Exception as e:
        return {"status": 400, "message": str(e)}

@record_router.get("/delete/{record_id}")
async def delete_record(
    record_id: int = None,
    user: dict = Depends(get_current_user)
):
    try:
        await psql_delete_record(record_id, user['id'])
        return {"status": 200, "message": "Deleted Record Successfully"}
    except Exception as e:
        return {"status": 500, "message": str(e)}