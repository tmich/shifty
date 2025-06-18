from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from uuid import UUID
from shifty.application.use_cases.user_service import UserService
from shifty.application.dto.user_dto import UserFull, UserCreate
from shifty.domain.entities import User
from shifty.infrastructure.db import get_session
from shifty.infrastructure.repositories.user_sqlalchemy import UserRepository

router = APIRouter(prefix="/users", tags=["users"])

def get_user_service(session = Depends(get_session)):
    return UserService(UserRepository(session))

@router.get("/", response_model=List[User])
def list_users(service: UserService = Depends(get_user_service)):
    return service.get_all()

@router.get("/{user_id}", response_model=UserFull)
def get_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    user = service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/", response_model=UserFull, status_code=201)
def create_user(user: UserCreate, service: UserService = Depends(get_user_service)):
    user_obj = User(**user.model_dump())
    return service.add(user_obj)

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    # service.delete(user_id)
    return Response(status_code=204)

@router.get("/role/{role}", response_model=List[UserFull])
def get_users_by_role(role: str, service: UserService = Depends(get_user_service)):
    return service.get_by_role(role)
