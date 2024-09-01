from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.dependencies import get_current_user
from app.database import psql_create_record, psql_get_record, psql_delete_record, psql_update_record, psql_get_all_records
from models.records import Record
from uuid import UUID

record_router = APIRouter(prefix="/records", tags=["Records"])

@record_router.post("/create")
async def create_record(
    record: Record,
    user: dict = Depends(get_current_user)
):
    try:
        await psql_create_record(record=record, user_id=str(user['id']))
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "success", "message": "Record created successfully"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": f"An unexpected error occurred: {str(e)}"}
        )

@record_router.get("/")
async def get_all_records(
    user: dict = Depends(get_current_user)
):
    try:
        records = await psql_get_all_records(user_id=str(user['id']))
        # Convert asyncpg.Record objects to dictionaries and ensure UUIDs are converted to strings
        serializable_records = [
            {key: str(value) if isinstance(value, UUID) else value for key, value in record.items()}
            for record in records
        ]
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "message": "Records retrieved successfully",
                "records": serializable_records
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "error", "message": str(e)}
        )

@record_router.get("/{record_id}")
async def get_record(
    record_id: str,
    user: dict = Depends(get_current_user)
):
    try:
        record = await psql_get_record(user_id=str(user['id']), record_id=str(record_id))
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "success", "message": record}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "error", "message": str(e)}
        )

@record_router.post("/{record_id}/update")
async def update_record(
    record_id: str,
    record_data: Record,
    user: dict = Depends(get_current_user)
):
    try:
        # Check if the record exists and belongs to the user
        await psql_get_record(user_id=str(user['id']), record_id=record_id)
        # Update the record
        await psql_update_record(record_id=record_id, user_id=str(user['id']), record_data=record_data)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "success", "message": "Record updated successfully"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "error", "message": str(e)}
        )

@record_router.delete("/{record_id}/delete")
async def delete_record(
    record_id: str,
    user: dict = Depends(get_current_user)
):
    try:
        await psql_delete_record(record_id=str(record_id), user_id=str(user['id']))
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "success", "message": "Deleted Record Successfully"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "error", "message": str(e)}
        )