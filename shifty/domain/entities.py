from dataclasses import dataclass
from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import date, datetime, time
from uuid import UUID


@dataclass
class User(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    role: Literal["worker", "admin"]
    is_active: bool = True


@dataclass
class Availability(BaseModel):
    id: UUID
    user_id: UUID
    date: date
    start_time: time
    end_time: time
    note: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)



@dataclass
class AvailabilitySlot(BaseModel):
    id: UUID
    user_id: UUID
    date: date
    start_time: time
    end_time: time
    note: Optional[str] = None
    created_at: datetime
