import enum
from typing import Literal, Optional, List
from pydantic import EmailStr
from sqlmodel import Column, Enum, Field, SQLModel, Relationship
from datetime import date, time, datetime, timedelta
import uuid


# class UserOrganization(SQLModel, table=True):
#     """
#     Represents the association between a user and an organization.
#     This model is used to link users to organizations they belong to.
#     """
#     __tablename__ = "user_organizations"  # type: ignore
#     user_id: uuid.UUID = Field(foreign_key="users.id", primary_key=True)
#     organization_id: uuid.UUID = Field(foreign_key="organizations.id", primary_key=True)


class UserBase(SQLModel):
    """
    Base model for User, used for creating and reading user data.
    This model includes fields that are common to both creating and reading user information.
    """
    full_name: str
    email: EmailStr
    role: str  # Literal["worker", "admin"]
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None


class User(UserBase, table=True):
    """
    Represents a user in the system.
    This model is used to store user information such as full name, email, role, and active status.
    """
    __tablename__ = "users"  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    organization_id: uuid.UUID = Field(
        foreign_key="organizations.id",
        sa_column_kwargs={"nullable": False}
    )

    availabilities: list["Availability"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    organization: Optional["Organization"] = Relationship(
        back_populates="users",
        #sa_relationship_kwargs={"foreign_keys": "[User.organization_id]"}
    )

    shifts: list["Shift"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "foreign_keys": "[Shift.user_id]"
        }
    )

    origin_shifts: list["Shift"] = Relationship(
        back_populates="origin_user",
        sa_relationship_kwargs={
            "foreign_keys": "[Shift.origin_user_id]"
        }
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
        back_populates="organization"
    )


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

    __mapper_args__ = {
        'polymorphic_identity': 'edge',
        'confirm_deleted_rows': False
    }



class ShiftStatus(str, enum.Enum):
    """
    Enum representing the status of a shift.
    """
    PENDING = "pending"
    TAKEN = "taken"
    CANCELED = "canceled"


class ShiftBase(SQLModel):
    user_id: uuid.UUID
    organization_id: uuid.UUID
    date: date
    start_time: time
    end_time: time
    note: Optional[str] = None
    created_at: datetime


class ShiftRead(ShiftBase):
    id: uuid.UUID
    origin_user_id: uuid.UUID
    status: ShiftStatus
    user: Optional[User] = None


class Shift(ShiftBase, table=True):
    """
    Represents a work shift assigned to a user in an organization.
    """
    __tablename__ = "shifts"  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="users.id")
    origin_user_id: uuid.UUID = Field(foreign_key="users.id")
    organization_id: uuid.UUID = Field(foreign_key="organizations.id")
    date: date
    start_time: time
    end_time: time
    note: Optional[str] = None
    status: ShiftStatus = Field(sa_column=Column(Enum(ShiftStatus)), default=ShiftStatus.PENDING)
    parent_shift_id: Optional[uuid.UUID] = Field(default=None, foreign_key="shifts.id")
    created_at: datetime = Field(default_factory=datetime.now)

    user: Optional["User"] = Relationship(
        back_populates="shifts",
        sa_relationship_kwargs={"foreign_keys": "[Shift.user_id]"}
    )

    origin_user: Optional["User"] = Relationship(
        back_populates="origin_shifts",
        sa_relationship_kwargs={"foreign_keys": "[Shift.origin_user_id]"}
    )
    
    overrides: list["Override"] = Relationship(
        back_populates="shift", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class ShiftType(SQLModel, table=True):
    """ Represents a shift type in an organization """
    
    __tablename__ = "shift_types"  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    organization_id: uuid.UUID = Field(foreign_key="organizations.id")
    name: str   # The name of the shift (e.g., "Morning")
    start_time: time = datetime.now().time()  # Start time of the shift
    end_time: time = (datetime.now() + timedelta(hours=8)).time()  # End time of the shift
    description: Optional[str] = None  # Additional description or notes
    expected_workers: int = Field(default=1)  # Minimum number of workers for this shift type
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
    user_id: uuid.UUID = Field(foreign_key="users.id")
    organization_id: uuid.UUID = Field(foreign_key="organizations.id")
    date: date
    start_time: time
    end_time: time
    taken_by_id: Optional[uuid.UUID] = Field(default=None, foreign_key="users.id")
    taken_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.now)
    is_taken: bool = Field(default=False)

    # Relationships (optional, for ORM navigation)
    shift: Optional[Shift] = Relationship(back_populates="overrides")
    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Override.user_id]"}, 
    )
    taken_by: Optional["User"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Override.taken_by_id]"})



class Auth(SQLModel, table=True):
    __tablename__ = "auth"  # type: ignore
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    is_valid: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
