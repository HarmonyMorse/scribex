from fastapi.testclient import TestClient
import pytest
from typing import Dict

def test_login(client):
    # First create a user
    client.post(
        "/api/users/teacher",
        json={
            "username": "test_login",
            "email": "login@test.com",
            "password": "testpass123",
            "profile": {
                "first_name": "Test",
                "last_name": "Login",
                "subject_areas": ["Math"],
                "grade_levels": [9, 10, 11]
            }
        }
    )
    
    # Then try to login
    response = client.post(
        "/api/auth/login",
        data={
            "username": "test_login",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data 

def test_login_success(client: TestClient, create_test_user: Dict):
    """Test successful login"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "fixture_user",
            "password": "StrongPass123!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"
    assert "refresh_token" in data

def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/auth/login",
        data={
            "username": "nonexistent_user",
            "password": "WrongPass123!"
        }
    )
    assert response.status_code == 401
    assert "detail" in response.json()

def test_refresh_token(client: TestClient, create_test_user: Dict):
    """Test token refresh"""
    # First login to get refresh token
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": "fixture_user",
            "password": "StrongPass123!"
        }
    )
    refresh_token = login_response.json()["refresh_token"]
    
    # Test token refresh
    response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "token_type" in data
    assert data["token_type"] == "bearer"

def test_refresh_token_invalid(client: TestClient):
    """Test refresh with invalid token"""
    response = client.post(
        "/api/auth/refresh",
        json={"refresh_token": "invalid_token"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()

def test_logout(client: TestClient, create_test_user: Dict):
    """Test logout functionality"""
    # First login to get token
    login_response = client.post(
        "/api/auth/login",
        data={
            "username": "fixture_user",
            "password": "StrongPass123!"
        }
    )
    token = login_response.json()["access_token"]
    
    # Test logout
    response = client.post(
        "/api/auth/logout",
        json={"token": token}
    )
    assert response.status_code == 200
    
    # Verify token is invalidated by trying to use it
    response = client.get(
        "/api/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401

def test_password_reset_request(client: TestClient, create_test_user: Dict):
    """Test password reset request"""
    response = client.post(
        "/api/auth/password-reset/request",
        json={
            "email": "fixture@example.com"
        }
    )
    assert response.status_code == 200
    
    # Test with non-existent email
    response = client.post(
        "/api/auth/password-reset/request",
        json={
            "email": "nonexistent@test.com"
        }
    )
    assert response.status_code == 404

def test_password_reset_confirm(client: TestClient, create_test_user: Dict):
    """Test password reset confirmation"""
    # Note: This test assumes we have a way to generate a valid reset token
    # In a real implementation, we'd need to mock the token generation
    
    response = client.post(
        "/api/auth/password-reset/confirm",
        json={
            "token": "valid_reset_token",
            "new_password": "NewStrongPass123!"
        }
    )
    assert response.status_code == 200
    
    # Test with invalid token
    response = client.post(
        "/api/auth/password-reset/confirm",
        json={
            "token": "invalid_token",
            "new_password": "NewStrongPass123!"
        }
    )
    assert response.status_code == 400

def test_change_password(client: TestClient, create_test_user: Dict):
    """Test password change"""
    token = create_test_user["token"]
    
    # Test successful password change
    response = client.post(
        "/api/auth/password/change",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "current_password": "StrongPass123!",
            "new_password": "NewStrongPass123!"
        }
    )
    assert response.status_code == 200
    
    # Test with wrong current password
    response = client.post(
        "/api/auth/password/change",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "current_password": "WrongPass123!",
            "new_password": "NewStrongPass123!"
        }
    )
    assert response.status_code == 400 