from fastapi import APIRouter, Depends, HTTPException
from shifty.application.use_cases.auth_service import AuthService
from shifty.infrastructure.db import get_admin_session
from shifty.application.dto.registration_dto import (
    RegisterOrgRequest, JoinOrgRequest, RegisterOrgResponse, TokenResponse
)
from shifty.application.use_cases.registration_service import RegistrationService
from shifty.infrastructure.repositories.auth_sqlalchemy import AuthRepository
from shifty.infrastructure.repositories.registration_sqlalchemy import RegistrationRepository
from shifty.infrastructure.repositories.user_sqlalchemy import UserRepository

# Using admin session for registration operations
# as it typically involves creating new organizations and users.
def get_registration_service(session=Depends(get_admin_session)):
    return RegistrationService(
        RegistrationRepository(session),
        UserRepository(session)
    )

def get_auth_service(session= Depends(get_admin_session)):
    return AuthService(AuthRepository(session))

router = APIRouter(prefix="/register", tags=["registration"])

@router.post("/organization", response_model=RegisterOrgResponse)
def register_organization(
    data: RegisterOrgRequest,
    service: RegistrationService = Depends(get_registration_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        org_code = service.register_organization(
            data.organization_name, data.user_email, data.user_password, data.full_name
        )
        
        # Authenticate the user to create a JWT token
        # after successfully registering the organization.
        auth = auth_service.signup(data.user_email, data.user_password)
        access_token = auth_service.create_jwt(str(auth.id))
        return RegisterOrgResponse(org_code=org_code, token=TokenResponse(access_token=access_token))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/join", response_model=TokenResponse)
def join_organization(
    data: JoinOrgRequest,
    service: RegistrationService = Depends(get_registration_service),
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        user = service.join_organization(
            data.org_code, data.user_email, data.user_password, data.full_name
        )
        
        auth = auth_service.signup(user.email, data.user_password)
        # auth_service.authenticate(data.user_email, data.user_password)
        access_token = auth_service.create_jwt(str(auth.id))
        return TokenResponse(access_token=access_token)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))