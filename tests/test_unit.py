"""Unit testovi - testiraju izoliranu logiku."""

from datetime import UTC, datetime, timedelta
from decimal import Decimal

from app.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from app.models.menu_item import MenuItem
from app.models.order import Order, OrderStatus
from app.models.user import User, UserRole


class TestPasswordHashing:
    """Testovi za hashiranje lozinki."""

    def test_hash_password(self):
        """Test da se lozinka pravilno hashira."""
        password = "mysecretpassword"
        hashed = get_password_hash(password)
        assert hashed != password
        assert len(hashed) > 20

    def test_verify_correct_password(self):
        """Test verifikacije ispravne lozinke."""
        password = "mysecretpassword"
        hashed = get_password_hash(password)
        assert verify_password(password, hashed) is True

    def test_verify_wrong_password(self):
        """Test verifikacije pogrešne lozinke."""
        password = "mysecretpassword"
        hashed = get_password_hash(password)
        assert verify_password("wrongpassword", hashed) is False

    def test_different_hashes_for_same_password(self):
        """Test da ista lozinka daje različite hashove (salt)."""
        password = "mysecretpassword"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        assert hash1 != hash2


class TestJWTToken:
    """Testovi za JWT tokene."""

    def test_create_access_token(self):
        """Test kreiranja access tokena."""
        data = {"sub": "testuser"}
        token = create_access_token(data)
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 50

    def test_create_token_with_expiry(self):
        """Test kreiranja tokena s custom istekom."""
        data = {"sub": "testuser"}
        expires = timedelta(minutes=60)
        token = create_access_token(data, expires_delta=expires)
        assert token is not None


class TestUserModel:
    """Testovi za User model."""

    def test_user_creation(self):
        """Test kreiranja User objekta."""
        user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="hashedpass",
            role=UserRole.USER,
        )
        assert user.username == "testuser"
        assert user.role == UserRole.USER
        assert user.is_active is True

    def test_admin_role(self):
        """Test admin uloge."""
        admin = User(
            username="admin",
            email="admin@example.com",
            hashed_password="hashedpass",
            role=UserRole.ADMIN,
        )
        assert admin.role == UserRole.ADMIN

    def test_user_default_values(self):
        """Test default vrijednosti za User."""
        user = User(
            username="user",
            email="user@example.com",
            hashed_password="hash",
        )
        assert user.is_active is True
        assert user.role == UserRole.USER
        assert user.full_name is None


class TestMenuItemModel:
    """Testovi za MenuItem model."""

    def test_menu_item_creation(self):
        """Test kreiranja MenuItem objekta."""
        item = MenuItem(
            name="Ćevapi",
            description="10 ćevapa s lukom",
            price=Decimal("8.00"),
            category="Glavna jela",
        )
        assert item.name == "Ćevapi"
        assert item.price == Decimal("8.00")
        assert item.is_available is True

    def test_menu_item_unavailable(self):
        """Test nedostupnog artikla."""
        item = MenuItem(
            name="Pohani šnicl",
            price=Decimal("7.00"),
            is_available=False,
        )
        assert item.is_available is False

    def test_menu_item_default_availability(self):
        """Test default dostupnosti."""
        item = MenuItem(name="Test", price=Decimal("1.00"))
        assert item.is_available is True


class TestOrderModel:
    """Testovi za Order model."""

    def test_order_creation(self):
        """Test kreiranja Order objekta."""
        pickup = datetime.now(UTC) + timedelta(hours=1)
        order = Order(
            user_id=1,
            pickup_time=pickup,
            total_price=Decimal("15.50"),
        )
        assert order.user_id == 1
        assert order.status == OrderStatus.PENDING
        assert order.total_price == Decimal("15.50")

    def test_order_status_transitions(self):
        """Test promjena statusa narudžbe."""
        order = Order(
            user_id=1,
            pickup_time=datetime.now(UTC) + timedelta(hours=1),
            total_price=Decimal("10.00"),
        )
        assert order.status == OrderStatus.PENDING

        order.status = OrderStatus.CONFIRMED
        assert order.status == OrderStatus.CONFIRMED

        order.status = OrderStatus.READY
        assert order.status == OrderStatus.READY

        order.status = OrderStatus.COMPLETED
        assert order.status == OrderStatus.COMPLETED

    def test_order_cancelled_status(self):
        """Test otkazane narudžbe."""
        order = Order(
            user_id=1,
            pickup_time=datetime.now(UTC) + timedelta(hours=1),
            total_price=Decimal("5.00"),
        )
        order.status = OrderStatus.CANCELLED
        assert order.status == OrderStatus.CANCELLED


class TestPriceCalculation:
    """Testovi za kalkulaciju cijena."""

    def test_total_price_single_item(self):
        """Test ukupne cijene s jednim artiklom."""
        price = Decimal("8.50")
        quantity = 1
        total = price * quantity
        assert total == Decimal("8.50")

    def test_total_price_multiple_items(self):
        """Test ukupne cijene s više artikala."""
        items = [
            (Decimal("8.00"), 2),  # 16.00
            (Decimal("2.50"), 1),  # 2.50
            (Decimal("3.00"), 3),  # 9.00
        ]
        total = sum(price * qty for price, qty in items)
        assert total == Decimal("27.50")

    def test_decimal_precision(self):
        """Test preciznosti decimalnih brojeva."""
        price = Decimal("7.99")
        quantity = 3
        total = price * quantity
        assert total == Decimal("23.97")
