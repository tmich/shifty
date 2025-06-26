from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from shifty.domain.entities import Auth
from shifty.infrastructure.db import get_admin_session
from shifty.infrastructure.repositories.auth_sqlalchemy import AuthRepository
from shifty.application.use_cases.auth_service import AuthService
from shifty.application.dto.auth_dto import SignupRequest, LoginRequest, TokenResponse
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service(session: Session = Depends(get_admin_session)):
    return AuthService(AuthRepository(session))

@router.post("/signup", response_model=TokenResponse, status_code=201)
def signup(data: SignupRequest, service: AuthService = Depends(get_auth_service)):
    auth: Auth = service.signup(data.username, data.password)
    token = service.create_jwt(str(auth.id))
    refresh_token = auth.refresh_token if auth.refresh_token is not None else ""
    token_response = TokenResponse(access_token=token, refresh_token=refresh_token)
    return token_response

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, service: AuthService = Depends(get_auth_service)):
    try:
        auth: Auth = service.authenticate(data.username, data.password)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = service.create_jwt(str(auth.id))
    refresh_token = auth.refresh_token if auth.refresh_token is not None else ""
    return TokenResponse(access_token=token, refresh_token=refresh_token)

class RefreshRequest(BaseModel):
    username: str
    refresh_token: str

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(data: RefreshRequest, service: AuthService = Depends(get_auth_service)):
    auth = service.verify_refresh_token(data.username, data.refresh_token)
    if not auth:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    # Rotate refresh token
    new_refresh_token, _ = service.rotate_refresh_token(auth)
    access_token = service.create_jwt(str(auth.id))
    return TokenResponse(access_token=access_token, refresh_token=new_refresh_token)
