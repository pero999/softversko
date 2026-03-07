"""Order model - narudžbe."""

from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel


def utc_now() -> datetime:
    """Vrati trenutno UTC vrijeme."""
    return datetime.now(UTC)


class OrderStatus(str, Enum):
    """Status narudžbe."""

    PENDING = "pending"
    CONFIRMED = "confirmed"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class OrderItemBase(SQLModel):
    """Bazni OrderItem model."""

    menu_item_id: int = Field(foreign_key="menu_items.id")
    quantity: int = Field(ge=1, default=1)
    unit_price: Decimal = Field(ge=0, decimal_places=2)


class OrderItem(OrderItemBase, table=True):
    """OrderItem database model - stavka narudžbe."""

    __tablename__ = "order_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")

    # Relationships
    order: Optional["Order"] = Relationship(back_populates="items")


class OrderBase(SQLModel):
    """Bazni Order model."""

    pickup_time: datetime
    note: Optional[str] = Field(default=None, max_length=500)


class Order(OrderBase, table=True):
    """Order database model - narudžba."""

    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    status: OrderStatus = Field(default=OrderStatus.PENDING)
    total_price: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    created_at: datetime = Field(default_factory=utc_now)
    updated_at: datetime = Field(default_factory=utc_now)

    # Relationships
    items: list[OrderItem] = Relationship(back_populates="order")


# Request/Response modeli


class OrderItemCreate(SQLModel):
    """Model za kreiranje stavke narudžbe."""

    menu_item_id: int
    quantity: int = Field(ge=1, default=1)


class OrderCreate(SQLModel):
    """Model za kreiranje narudžbe."""

    pickup_time: datetime
    note: Optional[str] = Field(default=None, max_length=500)
    items: list[OrderItemCreate]


class OrderItemRead(SQLModel):
    """Model za čitanje stavke narudžbe."""

    id: int
    menu_item_id: int
    quantity: int
    unit_price: Decimal
    menu_item_name: Optional[str] = None


class OrderRead(SQLModel):
    """Model za čitanje narudžbe."""

    id: int
    user_id: int
    pickup_time: datetime
    note: Optional[str]
    status: OrderStatus
    total_price: Decimal
    created_at: datetime
    items: list[OrderItemRead] = []


class OrderStatusUpdate(SQLModel):
    """Model za ažuriranje statusa narudžbe."""

    status: OrderStatus
