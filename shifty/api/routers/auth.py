from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from shifty.domain.entities import Auth
from shifty.infrastructure.db import get_admin_session
from shifty.infrastructure.repositories.auth_sqlalchemy import AuthRepository
from shifty.application.use_cases.auth_service import AuthService
from shifty.application.dto.auth_dto import SignupRequest, LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service(session: Session = Depends(get_admin_session)):
    return AuthService(AuthRepository(session))

@router.post("/signup", response_model=TokenResponse, status_code=201)
def signup(data: SignupRequest, service: AuthService = Depends(get_auth_service)):
    auth: Auth = service.signup(data.username, data.password)
    token = service.create_jwt(str(auth.id))
    return TokenResponse(access_token=token)

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, service: AuthService = Depends(get_auth_service)):
    try:
        auth: Auth = service.authenticate(data.username, data.password)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    token = service.create_jwt(str(auth.id))
    return TokenResponse(access_token=token)
