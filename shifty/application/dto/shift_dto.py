from datetime import date, time, datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class ShiftCreate(BaseModel):
    user_id: UUID
    organization_id: UUID
    date: date
    start_time: time
    end_time: time
    note: Optional[str] = None

class ShiftRead(BaseModel):
    id: UUID
    user_id: UUID
    organization_id: UUID
    date: date
    start_time: time
    end_time: time
    note: Optional[str] = None
    created_at: datetime