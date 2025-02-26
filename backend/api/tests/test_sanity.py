from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_sanity():
    """Basic test to verify pytest is working"""
    assert True is True

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "database" in data
    assert "environment" in data 