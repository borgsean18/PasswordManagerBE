from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.user import user_router
from app.record import record_router
from app.group import group_router
from app.security import security_router

app = FastAPI(
    title="Password Manager",
    version="1"
)

app.include_router(user_router)
app.include_router(record_router)
app.include_router(group_router)
app.include_router(security_router)

origins = [
    "http://127.0.0.1:8080",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def app_root():
    try:
        return {"message": "Hello World"}
    except SystemError as e:
        raise HTTPException(
            status_code=404, 
            detail=str(e)
        )