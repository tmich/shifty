import uuid
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """
    Represents a user in the system.
    This model is used to store user information such as full name, email, role, and active status.
    """
    id: uuid.UUID
    full_name: str
    email: EmailStr
    role: str #Literal["worker", "admin"]
    is_active: bool