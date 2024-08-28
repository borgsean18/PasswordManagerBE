from fastapi import HTTPException, Header
from typing import Annotated
from app.security import auth
from app.database import psql_search_user

async def get_current_user(
    auth_token: Annotated[str, Header()],
    user_email: Annotated[str, Header()]
):
    try:
        await auth(auth_token=auth_token, user_email=user_email)
        user = await psql_search_user(user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail="Authentication failed")