from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Response
from typing import List
from sqlmodel import Session

from shifty.application.dto.override_dto import OverrideCreate, OverrideRead, OverrideTake
from shifty.domain.entities import Override, ShiftRead
from shifty.infrastructure.db import get_session
from shifty.infrastructure.repositories.override_sqlalchemy import OverrideRepository
from shifty.infrastructure.repositories.shift_sqlalchemy import ShiftRepository
from shifty.application.use_cases.override_service import OverrideService
from shifty.domain.exceptions import InvalidOverrideException

router = APIRouter(prefix="/overrides", tags=["overrides"])

def get_override_service(
    session: Session = Depends(get_session)
):
    return OverrideService(
        OverrideRepository(session),
        ShiftRepository(session)
    )

@router.post("/", response_model=OverrideRead, status_code=201)
def create_override(
    data: OverrideCreate,
    service: OverrideService = Depends(get_override_service)
):
    try:
        return service.create(data)
    except InvalidOverrideException as ex:
        raise HTTPException(status_code=400, detail=str(ex))

@router.get("/", response_model=List[OverrideRead])
def list_overrides(service: OverrideService = Depends(get_override_service)):
    return service.list_all()

@router.get("/open", response_model=List[OverrideRead])
def list_open_overrides(service: OverrideService = Depends(get_override_service)):
    return service.list_open()

@router.get("/{override_id}", response_model=OverrideRead)
def get_override(override_id: UUID, service: OverrideService = Depends(get_override_service)):
    try:
        return service.get_by_id(override_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Override not found")

@router.post("/{override_id}/take", response_model=List[ShiftRead])
def take_override(
    override_id: UUID,
    data: OverrideTake,
    service: OverrideService = Depends(get_override_service)
):
    try:
        return service.take(override_id, data)
    except (ValueError, InvalidOverrideException) as ex:
        raise HTTPException(status_code=400, detail=str(ex))

@router.options("/")
def options_overrides():
    return Response(status_code=204, headers={
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
        "Access-Control-Allow-Headers": "*"
    })