from fastapi import APIRouter, Response as fastapiResponse, status
from fastapi.responses import JSONResponse
from models.user import LoginUser, LoginResponse, User, Response
from app.database_functions import psql_create_user, psql_search_user
from app.access_token import create_access_token

user_router = APIRouter(prefix="/user", tags=["User"])

@user_router.post("/login", response_model=LoginResponse)
async def login(user: LoginUser, response: fastapiResponse):
    try:
        result = await psql_search_user(user.email)

        if not result:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"status": "fail", "message": "Account not found"}
            )
        
        if (user.password != result["password"]):
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"status": "fail", "message": "Incorrect password"}
            )

        access_token = create_access_token(
            data={"email": result["email"]}
        )

        # Create a cookie for the Token
        response.set_cookie(key="Token", value=access_token)
        response.set_cookie(key="email", value=result["email"])

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": "success",
                "message": "Login successful",
                "access_token": access_token,
                "token_type": "bearer",
            }
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": f"An unexpected error occurred: {str(e)}"}
        )

@user_router.post("/create", response_model=Response)
async def create_account(user: User):
    try:
        result = await psql_search_user(user.email)
        if result is None:
            result = await psql_create_user(user=user)
            if result:
                return JSONResponse(
                    status_code=status.HTTP_201_CREATED,
                    content={"status": "success", "message": "User created successfully"}
                )
            else:
                return JSONResponse(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    content={"status": "error", "message": "Failed to create user"}
                )
        else:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"status": "fail", "message": "Email address already taken"}
            )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": f"An unexpected error occurred: {str(e)}"}
        )