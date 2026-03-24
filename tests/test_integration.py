"""Integracijski testovi - testiraju cijeli API tok."""

from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from app.models.menu_item import MenuItem
from app.models.user import User


class TestAuthFlow:
    """Integracijski testovi za autentikaciju."""

    def test_register_and_login_flow(self, client: TestClient):
        """Test kompletnog toka registracije i prijave."""
        # 1. Registracija
        register_response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "newuser",
                "email": "newuser@example.com",
                "password": "password123",
                "full_name": "New User",
            },
        )
        assert register_response.status_code == 201
        user_data = register_response.json()
        assert user_data["username"] == "newuser"
        assert user_data["role"] == "user"

        # 2. Login
        login_response = client.post(
            "/api/v1/auth/login",
            data={"username": "newuser", "password": "password123"},
        )
        assert login_response.status_code == 200
        token_data = login_response.json()
        assert "access_token" in token_data
        assert token_data["token_type"] == "bearer"

        # 3. Dohvati trenutnog korisnika
        me_response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {token_data['access_token']}"},
        )
        assert me_response.status_code == 200
        assert me_response.json()["username"] == "newuser"


class TestOrderFlow:
    """Integracijski testovi za narudžbe - glavni tok aplikacije."""

    def test_complete_order_flow(
        self,
        client: TestClient,
        test_user: User,
        test_admin: User,
        user_token: str,
        admin_token: str,
        test_menu_item: MenuItem,
    ):
        """Test kompletnog toka narudžbe od kreiranja do završetka."""
        # 1. Korisnik pregledava jelovnik
        menu_response = client.get("/api/v1/menu/")
        assert menu_response.status_code == 200
        menu = menu_response.json()
        assert len(menu) >= 1
        assert any(item["name"] == test_menu_item.name for item in menu)

        # 2. Korisnik kreira narudžbu
        pickup_time = (datetime.now(UTC) + timedelta(hours=2)).isoformat()
        order_response = client.post(
            "/api/v1/orders/",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "pickup_time": pickup_time,
                "note": "Bez soli molim",
                "items": [{"menu_item_id": test_menu_item.id, "quantity": 2}],
            },
        )
        assert order_response.status_code == 201
        order_data = order_response.json()
        assert order_data["status"] == "pending"
        assert order_data["total_price"] == str(test_menu_item.price * 2)
        order_id = order_data["id"]

        # 3. Korisnik pregledava svoje narudžbe
        my_orders_response = client.get(
            "/api/v1/orders/my",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert my_orders_response.status_code == 200
        my_orders = my_orders_response.json()
        assert len(my_orders) >= 1
        assert any(o["id"] == order_id for o in my_orders)

        # 4. Admin pregledava sve narudžbe
        all_orders_response = client.get(
            "/api/v1/orders/",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert all_orders_response.status_code == 200
        all_orders = all_orders_response.json()
        assert any(o["id"] == order_id for o in all_orders)

        # 5. Admin potvrđuje narudžbu
        confirm_response = client.patch(
            f"/api/v1/orders/{order_id}/status",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"status": "confirmed"},
        )
        assert confirm_response.status_code == 200
        assert confirm_response.json()["status"] == "confirmed"

        # 6. Admin označava narudžbu spremnom
        ready_response = client.patch(
            f"/api/v1/orders/{order_id}/status",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"status": "ready"},
        )
        assert ready_response.status_code == 200
        assert ready_response.json()["status"] == "ready"

        # 7. Admin označava narudžbu završenom
        complete_response = client.patch(
            f"/api/v1/orders/{order_id}/status",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"status": "completed"},
        )
        assert complete_response.status_code == 200
        assert complete_response.json()["status"] == "completed"


class TestMenuManagement:
    """Integracijski testovi za upravljanje jelovnikom."""

    def test_admin_menu_crud_flow(
        self, client: TestClient, admin_token: str, user_token: str
    ):
        """Test CRUD operacija na jelovniku (admin only)."""
        # 1. Admin kreira novi artikl
        create_response = client.post(
            "/api/v1/menu/",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "name": "Nova Pizza",
                "description": "Pizza s mozzarellom",
                "price": "9.99",
                "category": "Glavna jela",
                "is_available": True,
            },
        )
        assert create_response.status_code == 201
        item = create_response.json()
        item_id = item["id"]
        assert item["name"] == "Nova Pizza"

        # 2. Korisnik NE MOŽE kreirati artikl (403)
        user_create_response = client.post(
            "/api/v1/menu/",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "name": "Nedozvoljeno",
                "price": "5.00",
            },
        )
        assert user_create_response.status_code == 403

        # 3. Admin ažurira artikl
        update_response = client.patch(
            f"/api/v1/menu/{item_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={"price": "10.99", "is_available": False},
        )
        assert update_response.status_code == 200
        assert update_response.json()["price"] == "10.99"
        assert update_response.json()["is_available"] is False

        # 4. Admin briše artikl
        delete_response = client.delete(
            f"/api/v1/menu/{item_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert delete_response.status_code == 204

        # 5. Artikl više ne postoji
        get_response = client.get(f"/api/v1/menu/{item_id}")
        assert get_response.status_code == 404


class TestValidations:
    """Testovi za validacije i rubne slučajeve."""

    def test_order_unavailable_item_fails(
        self,
        client: TestClient,
        user_token: str,
        unavailable_menu_item: MenuItem,
    ):
        """Test da narudžba nedostupnog artikla vraća grešku."""
        pickup_time = (datetime.now(UTC) + timedelta(hours=2)).isoformat()
        response = client.post(
            "/api/v1/orders/",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "pickup_time": pickup_time,
                "items": [{"menu_item_id": unavailable_menu_item.id, "quantity": 1}],
            },
        )
        assert response.status_code == 400
        assert "nije dostupan" in response.json()["detail"]

    def test_order_past_pickup_time_fails(
        self,
        client: TestClient,
        user_token: str,
        test_menu_item: MenuItem,
    ):
        """Test da narudžba s prošlim vremenom preuzimanja vraća grešku."""
        past_time = (datetime.now(UTC) - timedelta(hours=1)).isoformat()
        response = client.post(
            "/api/v1/orders/",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "pickup_time": past_time,
                "items": [{"menu_item_id": test_menu_item.id, "quantity": 1}],
            },
        )
        assert response.status_code == 400
        assert "budućnosti" in response.json()["detail"]

    def test_unauthenticated_order_fails(
        self, client: TestClient, test_menu_item: MenuItem
    ):
        """Test da neautenticirani korisnik ne može kreirati narudžbu."""
        pickup_time = (datetime.now(UTC) + timedelta(hours=2)).isoformat()
        response = client.post(
            "/api/v1/orders/",
            json={
                "pickup_time": pickup_time,
                "items": [{"menu_item_id": test_menu_item.id, "quantity": 1}],
            },
        )
        assert response.status_code == 401
