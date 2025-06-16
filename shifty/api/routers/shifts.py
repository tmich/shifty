from uuid import UUID
from datetime import date, time, datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, Response, status
from sqlmodel import Session, select

from shifty.domain.entities import Shift
from shifty.infrastructure.db import get_session

router = APIRouter(prefix="/shifts", tags=["shifts"])

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