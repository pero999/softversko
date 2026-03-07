"""Testovi za main API."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_session
from main import app


# Test database setup
@pytest.fixture(name="session")
def session_fixture():
    """Kreiraj test database session."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
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


def test_root(client: TestClient):
    """Test root endpointa."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "docs" in data


def test_health_check(client: TestClient):
    """Test health check endpointa."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_create_user(client: TestClient):
    """Test kreiranja usera."""
    response = client.post(
        "/api/v1/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_create_user_duplicate_username(client: TestClient):
    """Test da dupli username vraća error."""
    # Kreiraj prvog usera
    client.post(
        "/api/v1/users/",
        json={"username": "duplicate", "email": "first@example.com"},
    )
    # Pokušaj kreirati drugog s istim username
    response = client.post(
        "/api/v1/users/",
        json={"username": "duplicate", "email": "second@example.com"},
    )
    assert response.status_code == 400


def test_read_users(client: TestClient):
    """Test dohvata svih usera."""
    # Kreiraj usera
    client.post(
        "/api/v1/users/",
        json={"username": "user1", "email": "user1@example.com"},
    )
    # Dohvati sve
    response = client.get("/api/v1/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_read_user(client: TestClient):
    """Test dohvata jednog usera."""
    # Kreiraj usera
    create_response = client.post(
        "/api/v1/users/",
        json={"username": "singleuser", "email": "single@example.com"},
    )
    user_id = create_response.json()["id"]

    # Dohvati po ID-u
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "singleuser"


def test_read_user_not_found(client: TestClient):
    """Test da nepostojeći user vraća 404."""
    response = client.get("/api/v1/users/99999")
    assert response.status_code == 404


def test_update_user(client: TestClient):
    """Test ažuriranja usera."""
    # Kreiraj usera
    create_response = client.post(
        "/api/v1/users/",
        json={"username": "updateme", "email": "update@example.com"},
    )
    user_id = create_response.json()["id"]

    # Ažuriraj
    response = client.patch(
        f"/api/v1/users/{user_id}",
        json={"full_name": "Updated Name"},
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"


def test_delete_user(client: TestClient):
    """Test brisanja usera."""
    # Kreiraj usera
    create_response = client.post(
        "/api/v1/users/",
        json={"username": "deleteme", "email": "delete@example.com"},
    )
    user_id = create_response.json()["id"]

    # Obriši
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204

    # Provjeri da ne postoji
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 404
