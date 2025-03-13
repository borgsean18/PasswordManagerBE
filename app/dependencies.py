from fastapi import Depends, HTTPException, status, Header
from typing import Annotated
from app.security import oauth2_scheme, decode_access_token
from app.database_functions import psql_search_user

async def get_current_user(
    auth_token: Annotated[str, Header()],
    user_email: Annotated[str, Header()]
):
    try:
        payload = decode_access_token(auth_token)
        if payload.get("email") != user_email:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        user = await psql_search_user(user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")