"""Osnovni testovi za API."""

from fastapi.testclient import TestClient


class TestHealthCheck:
    """Testovi za health check i root endpoint."""

    def test_root_endpoint(self, client: TestClient):
        """Test root endpointa."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "docs" in data
        assert "Menza" in data["message"]

    def test_health_check(self, client: TestClient):
        """Test health check endpointa."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestMenuPublicAccess:
    """Testovi za javni pristup jelovniku."""

    def test_get_menu_public(self, client: TestClient, test_menu_item):
        """Test da se jelovnik može dohvatiti bez autentikacije."""
        response = client.get("/api/v1/menu/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_get_single_item_public(self, client: TestClient, test_menu_item):
        """Test da se pojedini artikl može dohvatiti bez autentikacije."""
        response = client.get(f"/api/v1/menu/{test_menu_item.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == test_menu_item.name

    def test_filter_available_items(
        self, client: TestClient, test_menu_item, unavailable_menu_item
    ):
        """Test filtriranja samo dostupnih artikala."""
        response = client.get("/api/v1/menu/?available_only=true")
        assert response.status_code == 200
        data = response.json()
        item_ids = [item["id"] for item in data]
        assert test_menu_item.id in item_ids
        assert unavailable_menu_item.id not in item_ids


class TestAuthEndpoints:
    """Testovi za auth endpointe."""

    def test_register_user(self, client: TestClient):
        """Test registracije korisnika."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": "novikorisnik",
                "email": "novi@example.com",
                "password": "lozinka123",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "novikorisnik"
        assert data["role"] == "user"

    def test_register_duplicate_username(self, client: TestClient, test_user):
        """Test da dupli username vraća grešku."""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "username": test_user.username,
                "email": "drugi@example.com",
                "password": "lozinka123",
            },
        )
        assert response.status_code == 400
        assert "već postoji" in response.json()["detail"]

    def test_login_success(self, client: TestClient, test_user):
        """Test uspješnog logina."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": test_user.username, "password": "testpass123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

    def test_login_wrong_password(self, client: TestClient, test_user):
        """Test logina s pogrešnom lozinkom."""
        response = client.post(
            "/api/v1/auth/login",
            data={"username": test_user.username, "password": "wrongpass"},
        )
        assert response.status_code == 401

    def test_get_me(self, client: TestClient, test_user, user_token):
        """Test dohvaćanja trenutnog korisnika."""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        assert response.json()["username"] == test_user.username
