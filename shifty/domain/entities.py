from typing import Literal, Optional
import uuid
from pydantic import EmailStr
from sqlmodel import Field, SQLModel, Relationship
from datetime import date, time, datetime, timedelta


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

    shifts: list["Shift"] = Relationship(
        back_populates="user", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
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


class Shift(SQLModel, table=True):
    """
    Represents a work shift assigned to a user in an organization.
    """
    __tablename__ = "shifts"  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    organization_id: uuid.UUID = Field(foreign_key="organizations.id")
    date: date
    start_time: time
    end_time: time
    note: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(back_populates="shifts")
    overrides: list["Override"] = Relationship(
        back_populates="shift", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class ShiftType(SQLModel, table=True):
    """ Represents a shift type in an organization """
    
    __tablename__ = "shift_tp"  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    organization_id: uuid.UUID = Field(foreign_key="organizations.id")
    name: str   # The name of the shift (e.g., "Morning")
    start_time: time = datetime.now().time()  # Start time of the shift
    end_time: time = (datetime.now() + timedelta(hours=8)).time()  # End time of the shift
    description: Optional[str] = None  # Additional description or notes
    is_active: bool = Field(default=True) # Whether the slot is currently available
    created_at: datetime = Field(default_factory=datetime.now)  # When the slot was created
    updated_at: Optional[datetime] = None  # When the slot was last updated


class Override(SQLModel, table=True):
    """
    Represents a request to override (partially or totally) a shift by another user.
    """
    __tablename__ = "overrides"  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    shift_id: uuid.UUID = Field(foreign_key="shifts.id")
    requester_id: uuid.UUID = Field(foreign_key="users.id")
    date: date
    start_time: time
    end_time: time
    taken_by_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    taken_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    is_taken: bool = Field(default=False)

    # Relationships (optional, for ORM navigation)
    shift: Optional["Shift"] = Relationship(back_populates="overrides")
    requester: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Override.requester_id]"})
    taken_by: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Override.taken_by_id]"})


