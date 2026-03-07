"""User model s ulogama."""

from datetime import UTC, datetime
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Vrati trenutno UTC vrijeme."""
    return datetime.now(UTC)


class UserRole(str, Enum):
    """Korisničke uloge."""

    USER = "user"
    ADMIN = "admin"


class UserBase(SQLModel):
    """Bazni User model."""

    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    email: str = Field(index=True, unique=True)
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)
    role: UserRole = Field(default=UserRole.USER)


class User(UserBase, table=True):
    """User database model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field()
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class UserCreate(SQLModel):
    """Model za kreiranje usera."""

    username: str = Field(min_length=3, max_length=50)
    email: str
    password: str = Field(min_length=6)
    full_name: Optional[str] = None


class UserRead(SQLModel):
    """Model za čitanje usera."""

    id: int
    username: str
    email: str
    full_name: Optional[str]
    is_active: bool
    role: UserRole
    created_at: datetime


class Token(SQLModel):
    """JWT Token model."""

    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    """Token payload data."""

    username: Optional[str] = None
