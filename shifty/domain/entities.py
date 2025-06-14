from typing import Literal, Optional
import uuid
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship
from datetime import date, time, datetime


class UserOrganization(SQLModel, table=True):
    """
    Represents the association between a user and an organization.
    This model is used to link users to organizations they belong to.
    """
    __tablename__ = "user_organizations"  # type: ignore
    user_id: uuid.UUID = Field(foreign_key="users.id", primary_key=True)
    organization_id: uuid.UUID = Field(foreign_key="organizations.id", primary_key=True)


class User(SQLModel, table=True):
    """
    Represents a user in the system.
    This model is used to store user information such as full name, email, role, and active status.
    """
    __tablename__ = "users"  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    full_name: str
    email: EmailStr
    role: str #Literal["worker", "admin"]
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    
    availabilities: list["Availability"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    organizations: list["Organization"] = Relationship(
        back_populates="users",
        link_model=UserOrganization
    )


class Organization(SQLModel, table=True):
    """
    Represents an organization in the system.
    This model is used to store organization information such as name and description.
    """
    __tablename__ = "organizations"  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    users: Optional["User"] = Relationship(
        back_populates="organizations", 
        link_model=UserOrganization
    )
    # organization: Optional[Organization] = Relationship(back_populates="users")


class Availability(SQLModel, table=True):
    """
    Represents an availability record for a user.
    This model is used to store the availability of a user for a specific date and time range.
    """
    __tablename__ = "availabilities" # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    date: date
    start_time: time
    organization_id: uuid.UUID = Field(foreign_key="organizations.id")
    end_time: time
    note: Optional[str] = None
    created_at: datetime

    user: Optional["User"] = Relationship(back_populates="availabilities")


# class AvailabilitySlot(SQLModel, table=True):
#     """
#     Represents a time slot of availability for a user.
#     This model is used to store the start and end times of an availability slot for a specific user on a given date.
#     """

#     __tablename__ = "availability_slots" # type: ignore
#     id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     user_id: uuid.UUID = Field(foreign_key="users.id")
#     date: date
#     start_time: time
#     end_time: time
#     note: Optional[str] = None
#     created_at: datetime

#     user: Optional[User] = Relationship(back_populates="availabilities")



