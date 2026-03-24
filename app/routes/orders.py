"""Orders API rute - narudžbe."""

from datetime import UTC, datetime
from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.auth import get_current_active_user, get_current_admin
from app.database import get_session
from app.models.menu_item import MenuItem
from app.models.order import (
    Order,
    OrderCreate,
    OrderItem,
    OrderItemRead,
    OrderRead,
    OrderStatus,
    OrderStatusUpdate,
)
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["orders"])


def build_order_response(order: Order, session: Session) -> OrderRead:
    """Gradi OrderRead response s imenima artikala."""
    items_read = []
    for item in order.items:
        menu_item = session.get(MenuItem, item.menu_item_id)
        items_read.append(
            OrderItemRead(
                id=item.id,
                menu_item_id=item.menu_item_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                menu_item_name=menu_item.name if menu_item else None,
            )
        )
    return OrderRead(
        id=order.id,
        user_id=order.user_id,
        pickup_time=order.pickup_time,
        note=order.note,
        status=order.status,
        total_price=order.total_price,
        created_at=order.created_at,
        items=items_read,
    )


# ============ USER ENDPOINTI ============


@router.post("/", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    """Kreiraj novu narudžbu."""
    if not order_data.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Narudžba mora sadržavati barem jednu stavku",
        )

    # Validiraj vrijeme preuzimanja (mora biti u budućnosti)
    if order_data.pickup_time <= datetime.now(UTC):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vrijeme preuzimanja mora biti u budućnosti",
        )

    # Validiraj artikle i izračunaj cijenu
    total_price = Decimal("0.00")
    order_items = []

    for item_data in order_data.items:
        menu_item = session.get(MenuItem, item_data.menu_item_id)

        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Artikl s ID {item_data.menu_item_id} nije pronađen",
            )

        if not menu_item.is_available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Artikl '{menu_item.name}' trenutno nije dostupan",
            )

        item_total = menu_item.price * item_data.quantity
        total_price += item_total

        order_items.append(
            {
                "menu_item_id": menu_item.id,
                "quantity": item_data.quantity,
                "unit_price": menu_item.price,
            }
        )

    # Kreiraj narudžbu
    db_order = Order(
        user_id=current_user.id,
        pickup_time=order_data.pickup_time,
        note=order_data.note,
        total_price=total_price,
        status=OrderStatus.PENDING,
    )
    session.add(db_order)
    session.commit()
    session.refresh(db_order)

    # Kreiraj stavke narudžbe
    for item_data in order_items:
        db_item = OrderItem(order_id=db_order.id, **item_data)
        session.add(db_item)

    session.commit()
    session.refresh(db_order)

    return build_order_response(db_order, session)


@router.get("/my", response_model=list[OrderRead])
def get_my_orders(
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
    status_filter: OrderStatus | None = Query(None, alias="status"),
):
    """Dohvati moje narudžbe."""
    query = select(Order).where(Order.user_id == current_user.id)

    if status_filter:
        query = query.where(Order.status == status_filter)

    orders = session.exec(query.order_by(Order.created_at.desc())).all()
    return [build_order_response(order, session) for order in orders]


@router.get("/my/{order_id}", response_model=OrderRead)
def get_my_order(
    order_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    """Dohvati moju narudžbu po ID-u."""
    order = session.get(Order, order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Narudžba nije pronađena",
        )

    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nemate pristup ovoj narudžbi",
        )

    return build_order_response(order, session)


@router.delete("/my/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_my_order(
    order_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    session: Session = Depends(get_session),
):
    """Otkaži moju narudžbu (samo ako je PENDING)."""
    order = session.get(Order, order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Narudžba nije pronađena",
        )

    if order.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Nemate pristup ovoj narudžbi",
        )

    if order.status != OrderStatus.PENDING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Možete otkazati samo narudžbe sa statusom 'pending'",
        )

    order.status = OrderStatus.CANCELLED
    order.updated_at = datetime.now(UTC)
    session.add(order)
    session.commit()
    return None


# ============ ADMIN ENDPOINTI ============


@router.get("/", response_model=list[OrderRead])
def get_all_orders(
    current_admin: Annotated[User, Depends(get_current_admin)],
    session: Session = Depends(get_session),
    status_filter: OrderStatus | None = Query(None, alias="status"),
):
    """Dohvati sve narudžbe (samo admin)."""
    query = select(Order)

    if status_filter:
        query = query.where(Order.status == status_filter)

    orders = session.exec(query.order_by(Order.created_at.desc())).all()
    return [build_order_response(order, session) for order in orders]


@router.get("/{order_id}", response_model=OrderRead)
def get_order(
    order_id: int,
    current_admin: Annotated[User, Depends(get_current_admin)],
    session: Session = Depends(get_session),
):
    """Dohvati narudžbu po ID-u (samo admin)."""
    order = session.get(Order, order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Narudžba nije pronađena",
        )

    return build_order_response(order, session)


@router.patch("/{order_id}/status", response_model=OrderRead)
def update_order_status(
    order_id: int,
    status_update: OrderStatusUpdate,
    current_admin: Annotated[User, Depends(get_current_admin)],
    session: Session = Depends(get_session),
):
    """Ažuriraj status narudžbe (samo admin)."""
    order = session.get(Order, order_id)

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Narudžba nije pronađena",
        )

    order.status = status_update.status
    order.updated_at = datetime.now(UTC)
    session.add(order)
    session.commit()
    session.refresh(order)

    return build_order_response(order, session)
