import os
import pytest
from fastapi.testclient import TestClient
from typing import Generator, Dict

from app.main import app
from app.core.deps import get_db
from app.core.security import create_access_token, get_password_hash
from app.services.mock_user_service import MockUserService

# Create a global mock service instance for tests
mock_service = MockUserService()

@pytest.fixture
def client() -> Generator:
    """Test client fixture"""
    def override_get_db():
        try:
            yield mock_service
        finally:
            pass  # No cleanup needed for mock service
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def create_test_user(client: TestClient) -> Dict:
    """Create a test user and return user data with token"""
    user_data = {
        "username": "fixture_user",
        "email": "fixture@example.com",
        "password": "StrongPass123!",
        "profile": {
            "first_name": "Test",
            "last_name": "Teacher",
            "subject_areas": ["Math", "Science"],
            "grade_levels": [6, 7, 8]
        }
    }
    
    # Create user
    response = client.post("/api/users/teacher", json=user_data)
    assert response.status_code == 201
    user = response.json()
    
    # Login to get token
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": user_data["username"],
            "password": user_data["password"]
        }
    )
    assert login_response.status_code == 200
    tokens = login_response.json()
    
    return {**user, "token": tokens["access_token"]}

@pytest.fixture(autouse=True)
def setup_test_env():
    """Automatically set up test environment for all tests"""
    # Store original env vars
    original_env = dict(os.environ)
    
    # Set test environment variables
    os.environ["TESTING"] = "1"
    os.environ["JWT_SECRET_KEY"] = "test_secret_key_123"
    os.environ["JWT_ALGORITHM"] = "HS256"
    os.environ["OPENAI_API_KEY"] = "test_openai_key_123"
    os.environ["SAPLING_API_KEY"] = "test_sapling_key_123"
    os.environ["WHISPER_API_KEY"] = "test_whisper_key_123"
    
    # Clear mock service data before each test
    mock_service.users.clear()
    
    yield
    
    # Restore original env vars
    os.environ.clear()
    os.environ.update(original_env) 