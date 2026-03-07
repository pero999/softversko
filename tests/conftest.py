"""Pytest konfiguracija i fixtures."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.auth import create_access_token, get_password_hash
from app.database import get_session
from app.models.menu_item import MenuItem
from app.models.order import Order, OrderItem, OrderStatus
from app.models.user import User, UserRole
from main import app


@pytest.fixture(name="engine")
def engine_fixture():
    """Kreiraj test database engine."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture(name="session")
def session_fixture(engine):
    """Kreiraj test database session."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    """Kreiraj test client s test database."""

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session) -> User:
    """Kreiraj test korisnika."""
    user = User(
        username="testuser",
        email="test@example.com",
        full_name="Test User",
        hashed_password=get_password_hash("testpass123"),
        role=UserRole.USER,
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_admin")
def test_admin_fixture(session: Session) -> User:
    """Kreiraj test admina."""
    admin = User(
        username="testadmin",
        email="admin@example.com",
        full_name="Test Admin",
        hashed_password=get_password_hash("adminpass123"),
        role=UserRole.ADMIN,
        is_active=True,
    )
    session.add(admin)
    session.commit()
    session.refresh(admin)
    return admin


@pytest.fixture(name="user_token")
def user_token_fixture(test_user: User) -> str:
    """Kreiraj JWT token za test korisnika."""
    return create_access_token(data={"sub": test_user.username})


@pytest.fixture(name="admin_token")
def admin_token_fixture(test_admin: User) -> str:
    """Kreiraj JWT token za test admina."""
    return create_access_token(data={"sub": test_admin.username})


@pytest.fixture(name="test_menu_item")
def test_menu_item_fixture(session: Session) -> MenuItem:
    """Kreiraj test artikl."""
    item = MenuItem(
        name="Test Jelo",
        description="Opis test jela",
        price=Decimal("5.50"),
        category="Glavna jela",
        is_available=True,
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@pytest.fixture(name="unavailable_menu_item")
def unavailable_menu_item_fixture(session: Session) -> MenuItem:
    """Kreiraj nedostupan test artikl."""
    item = MenuItem(
        name="Nedostupno Jelo",
        description="Ovo jelo nije dostupno",
        price=Decimal("10.00"),
        category="Glavna jela",
        is_available=False,
    )
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@pytest.fixture(name="test_order")
def test_order_fixture(
    session: Session, test_user: User, test_menu_item: MenuItem
) -> Order:
    """Kreiraj test narudžbu."""
    order = Order(
        user_id=test_user.id,
        pickup_time=datetime.now(UTC) + timedelta(hours=2),
        note="Test narudžba",
        status=OrderStatus.PENDING,
        total_price=test_menu_item.price,
    )
    session.add(order)
    session.commit()
    session.refresh(order)

    order_item = OrderItem(
        order_id=order.id,
        menu_item_id=test_menu_item.id,
        quantity=1,
        unit_price=test_menu_item.price,
    )
    session.add(order_item)
    session.commit()
    session.refresh(order)

    return order
