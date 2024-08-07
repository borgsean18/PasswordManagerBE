from pydantic import BaseModel, field_validator, EmailStr

class User(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginUser(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, p: str):
        if (p == ""):
            raise ValueError('Password must not be left empty')
        return p


class Response(BaseModel):
    status: str
    message: str


class LoginResponse(Response):
    access_token: str
    token_type: str