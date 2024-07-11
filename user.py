from fastapi import APIRouter, status, HTTPException, Header
from fastapi.responses import JSONResponse
from models import LoginUser, LoginResponse, CreateUser, User, Response
from database import psql_create_user, psql_search_user
from access_token import create_access_token, decode_token

user_router = APIRouter(prefix="/user")

@user_router.post("/login", response_model=LoginResponse)
async def login(user: LoginUser):
    try:
        result = await psql_search_user(user.email)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        if (user.password != result["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect password"
            )
        
        # Successful login
        u = User(name=result['name'], email=result['email'], password=result['password'])

        access_token = create_access_token (
            data={"email": user.email}
        )

        return LoginResponse(
            status="success",
            message="Login successful",
            access_token=access_token,
            token_type="bearer",
            user_id=result["id"],
            name=u.name
        )
    
    except HTTPException as http_ex:
        return JSONResponse(
            status_code=http_ex.status_code,
            content={"status": "fail", "message": http_ex.detail}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": f"An unexpected error occurred: {str(e)}"}
        )
    

@user_router.post("/create", response_model=Response)
async def create_account(user: CreateUser):
    try:
        result = await psql_search_user(user.email)
        if (result is None):
            result = await psql_create_user(user.name[0], user.email, user.password[0])
            if result:
                return Response(
                    status="ok",
                    message="user created"
                )
            else:
                return Response(
                    status="fail",
                    message="failed to create user"
                )
        else:
            return Response(
                status="fail",
                message="Email address already in user"
            )
    
    except ValueError as e:
        raise ValueError(f"Error: {e}")
    

@user_router.get('/authenticate')
async def authenticate(
    authorization: str = Header(...)
):
    try:
        return decode_token(token=authorization)
    except Exception as e:
        pass