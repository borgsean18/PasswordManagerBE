from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from user import authenticate_user
from models import Password
from typing import Annotated
from database import psql_create_password

password_router = APIRouter(prefix="/password")

@password_router.post("/create")
async def create_password(
    password: Password,
    auth_token: Annotated[str | None, Header(...)] = None,
    user_email: Annotated[str | None, Header(...)] = None
    ):
    try:
        auth = await authenticate_user(auth_token=auth_token, user_email=user_email)

        # upload password to db
        result = psql_create_password(password)

        return {"message":"success"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "fail", "message": e}
        )


@password_router.get("/GetPassword/")
async def get_password(
    id: int
    ):
    return id