"""MenuItem model - artikli jelovnika."""

from datetime import UTC, datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    """Vrati trenutno UTC vrijeme."""
    return datetime.now(UTC)


class MenuItemBase(SQLModel):
    """Bazni MenuItem model."""

    name: str = Field(index=True, min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    price: Decimal = Field(ge=0, decimal_places=2)
    is_available: bool = Field(default=True)
    category: Optional[str] = Field(default=None, max_length=50)


class MenuItem(MenuItemBase, table=True):
    """MenuItem database model."""

    __tablename__ = "menu_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)


class MenuItemCreate(MenuItemBase):
    """Model za kreiranje artikla."""

    pass


class MenuItemUpdate(SQLModel):
    """Model za ažuriranje artikla."""

    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    price: Optional[Decimal] = Field(default=None, ge=0)
    is_available: Optional[bool] = None
    category: Optional[str] = Field(default=None, max_length=50)


class MenuItemRead(MenuItemBase):
    """Model za čitanje artikla."""

    id: int
    created_at: datetime
    updated_at: datetime
