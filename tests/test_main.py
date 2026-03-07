from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_health_check():
    """Test da API radi."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root():
    """Test root endpointa."""
    response = client.get("/")
    assert response.status_code == 200
