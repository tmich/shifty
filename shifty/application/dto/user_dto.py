from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime


class UserFull(BaseModel):
    id: UUID
    organization_id: UUID
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime
    updated_at: datetime | None = None

    class ConfigDict:
        from_attributes = True


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    role: str
    is_active: bool = True
    organization_id: UUID
