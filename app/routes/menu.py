"""Menu API rute - javni jelovnik i admin CRUD."""

from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from app.auth import get_current_admin
from app.database import get_session
from app.models.menu_item import MenuItem, MenuItemCreate, MenuItemRead, MenuItemUpdate
from app.models.user import User

router = APIRouter(prefix="/menu", tags=["menu"])


# ============ JAVNI ENDPOINTI ============


@router.get("/", response_model=list[MenuItemRead])
def get_menu(
    session: Session = Depends(get_session),
    available_only: bool = Query(True, description="Prikaži samo dostupne artikle"),
    category: str | None = Query(None, description="Filtriraj po kategoriji"),
):
    """Dohvati jelovnik (javno dostupno)."""
    query = select(MenuItem)

    if available_only:
        query = query.where(MenuItem.is_available.is_(True))

    if category:
        query = query.where(MenuItem.category == category)

    items = session.exec(query.order_by(MenuItem.category, MenuItem.name)).all()
    return items


@router.get("/{item_id}", response_model=MenuItemRead)
def get_menu_item(item_id: int, session: Session = Depends(get_session)):
    """Dohvati pojedini artikl (javno dostupno)."""
    item = session.get(MenuItem, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artikl nije pronađen",
        )
    return item


# ============ ADMIN ENDPOINTI ============


@router.post("/", response_model=MenuItemRead, status_code=status.HTTP_201_CREATED)
def create_menu_item(
    item: MenuItemCreate,
    current_admin: Annotated[User, Depends(get_current_admin)],
    session: Session = Depends(get_session),
):
    """Kreiraj novi artikl (samo admin)."""
    db_item = MenuItem.model_validate(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


@router.patch("/{item_id}", response_model=MenuItemRead)
def update_menu_item(
    item_id: int,
    item_update: MenuItemUpdate,
    current_admin: Annotated[User, Depends(get_current_admin)],
    session: Session = Depends(get_session),
):
    """Ažuriraj artikl (samo admin)."""
    item = session.get(MenuItem, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artikl nije pronađen",
        )

    item_data = item_update.model_dump(exclude_unset=True)
    for key, value in item_data.items():
        setattr(item, key, value)

    item.updated_at = datetime.now(UTC)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item(
    item_id: int,
    current_admin: Annotated[User, Depends(get_current_admin)],
    session: Session = Depends(get_session),
):
    """Obriši artikl (samo admin)."""
    item = session.get(MenuItem, item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artikl nije pronađen",
        )

    session.delete(item)
    session.commit()
    return None
