from pydantic import BaseModel, EmailStr

class RegisterOrgRequest(BaseModel):
    organization_name: str
    user_email: EmailStr
    user_password: str
    full_name: str

class JoinOrgRequest(BaseModel):
    org_code: str
    user_email: EmailStr
    user_password: str
    full_name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterOrgResponse(BaseModel):
    org_code: str
    token: TokenResponse