"""User model."""

from datetime import UTC, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Vrati trenutno UTC vrijeme."""
    return datetime.now(UTC)


class UserBase(SQLModel):
    """Bazni User model."""

    username: str = Field(index=True, unique=True, min_length=3, max_length=50)
    email: str = Field(index=True, unique=True)
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """User database model."""

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class UserCreate(UserBase):
    """Model za kreiranje usera."""

    pass


class UserUpdate(SQLModel):
    """Model za update usera."""

    username: Optional[str] = Field(default=None, min_length=3, max_length=50)
    email: Optional[str] = None
    full_name: Optional[str] = Field(default=None, max_length=100)
    is_active: Optional[bool] = None


class UserRead(UserBase):
    """Model za čitanje usera."""

    id: int
    created_at: datetime
    updated_at: datetime
