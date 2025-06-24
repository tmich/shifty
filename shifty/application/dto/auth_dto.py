from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    username: EmailStr
    password: str

class LoginRequest(BaseModel):
    username: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
