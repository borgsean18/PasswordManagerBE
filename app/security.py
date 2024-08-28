from fastapi import APIRouter, status, Header
from typing import Annotated
from fastapi.responses import JSONResponse
from app.access_token import decode_token

security_router = APIRouter(prefix="/security", tags=["security"])

@security_router.get("/auth")
async def auth(
    auth_token: Annotated[str | None, Header()] = None,
    user_email: Annotated[str | None, Header()] = None
):
    try:
        if auth_token is None or user_email is None:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"status": "fail", "message": "Missing auth token or user email"}
            )

        if user_email == decode_token(auth_token)['email']:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"status": "success", "message": "Authentication successful"}
            )
        
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"status": "fail", "message": "Authentication failed"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": f"An unexpected error occurred: {str(e)}"}
        )