from uuid import UUID
from datetime import date, time, datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session, select

from shifty.domain.entities import Shift
from shifty.application.dto.shift_dto import ShiftCreate, ShiftRead
from shifty.application.use_cases.shift_service import ShiftService
from shifty.infrastructure.repositories.shift_sqlalchemy import ShiftRepository
from shifty.infrastructure.db import get_session

router = APIRouter(prefix="/shifts", tags=["shifts"])

# Dependency
def get_shift_service(session=Depends(get_session)):
    return ShiftService(ShiftRepository(session))

@router.post("/", response_model=Shift, status_code=201)
def create_shift(
    shift: Shift,
    session: Session = Depends(get_session)
):
    session.add(shift)
    session.commit()
    session.refresh(shift)
    return shift

@router.get("/", response_model=List[Shift])
def list_shifts(session: Session = Depends(get_session)):
    shifts = session.exec(select(Shift)).all()
    return shifts

@router.get("/{shift_id}", response_model=Optional[Shift])
def get_shift(shift_id: UUID, response: Response, session: Session = Depends(get_session)):
    shift = session.get(Shift, shift_id)
    if not shift:
        if response:
            response.status_code = status.HTTP_404_NOT_FOUND
        return None
    return shift

@router.delete("/{shift_id}", status_code=204)
def delete_shift(shift_id: UUID, response: Response, session: Session = Depends(get_session)):
    shift = session.get(Shift, shift_id)
    if not shift:
        if response:
            response.status_code = status.HTTP_404_NOT_FOUND
        return
    session.delete(shift)
    session.commit()

@router.get("/date/{date}", response_model=List[ShiftRead])
def get_shifts_by_date(date: date, service: ShiftService = Depends(get_shift_service)):
    return service.get_by_date(date)

@router.get("/user/{user_id}", response_model=List[ShiftRead])
def get_shifts_by_user(user_id: UUID, service: ShiftService = Depends(get_shift_service)):
    return service.get_by_user(user_id)

@router.get("/user/{user_id}/date/{date}", response_model=List[ShiftRead])
def get_shifts_by_user_and_date(user_id: UUID, date: date, service: ShiftService = Depends(get_shift_service)):
    return service.get_by_user_and_date(user_id, date)

@router.put("/{shift_id}", response_model=ShiftRead)
def update_shift(
    shift_id: UUID,
    data: ShiftCreate,
    service: ShiftService = Depends(get_shift_service)
):
    updated = service.update(shift_id, data.dict(exclude_unset=True))
    return updated