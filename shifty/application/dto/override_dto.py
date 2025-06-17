from datetime import date, time, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class OverrideCreate(BaseModel):
    shift_id: UUID
    requester_id: UUID
    date: date
    start_time: time
    end_time: time

class OverrideRead(BaseModel):
    id: UUID
    shift_id: UUID
    requester_id: UUID
    date: date
    start_time: time
    end_time: time
    taken_by_id: Optional[UUID]
    taken_at: Optional[datetime]
    created_at: datetime
    is_taken: bool

class OverrideTake(BaseModel):
    taken_by_id: UUID