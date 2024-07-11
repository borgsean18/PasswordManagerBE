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
    
class CreateUser(User):
    @field_validator('name', 'password')
    @classmethod
    def validate_fields(cls, n: str, p: str):
        if (n == "" or p == ""):
            raise ValueError('Cant leave fields empty')
        return n,p
    
class Response(BaseModel):
    status: str
    message: str


class LoginResponse(Response):
    access_token: str
    token_type: str
    user_id: int
    name: str