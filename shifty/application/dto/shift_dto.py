from datetime import date, time, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from sqlmodel import SQLModel
from shifty.application.dto.user_dto import User
from shifty.domain.entities import ShiftStatus



class ShiftCreate(BaseModel):
    user_id: UUID
    origin_user_id: UUID
    organization_id: UUID
    date: date
    start_time: time
    end_time: time
    note: Optional[str] = None

