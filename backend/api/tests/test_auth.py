import pytest
import pytest_asyncio
from httpx import AsyncClient
from datetime import datetime, timedelta, UTC
from uuid import uuid4

from app.main import app
from app.core.security import create_access_token, create_refresh_token, get_password_hash
from app.models.user import User
from app.core.config import settings

@pytest.fixture
def test_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123!"
    }

@pytest_asyncio.fixture
async def test_user_in_db(test_user_data, db_session):
    user = User(
        id=uuid4(),
        username=test_user_data["username"],
        email=test_user_data["email"],
        hashed_password=get_password_hash(test_user_data["password"]),
        is_active=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user_in_db: User, test_user_data: dict):
    """Test successful login with valid credentials"""
    response = await client.post(
        "/auth/login",
        data={  # Using form data as OAuth2 expects
            "username": test_user_data["username"],
            "password": test_user_data["password"]
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert isinstance(data["expires_in"], int)

@pytest.mark.asyncio
async def test_login_invalid_password(client: AsyncClient, test_user_in_db: User, test_user_data: dict):
    """Test login with invalid password"""
    response = await client.post(
        "/auth/login",
        data={
            "username": test_user_data["username"],
            "password": "wrongpassword"
        }
    )
    assert response.status_code == 401
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_login_invalid_username(client: AsyncClient, test_user_in_db: User):
    """Test login with non-existent username"""
    response = await client.post(
        "/auth/login",
        data={
            "username": "nonexistent",
            "password": "somepassword"
        }
    )
    assert response.status_code == 401
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_protected_route_with_token(client: AsyncClient, test_user_in_db: User):
    """Test accessing protected route with valid token"""
    token = create_access_token(test_user_in_db.id)
    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user_in_db.username
    assert data["email"] == test_user_in_db.email

@pytest.mark.asyncio
async def test_protected_route_no_token(client: AsyncClient):
    """Test accessing protected route without token"""
    response = await client.get("/users/me")
    assert response.status_code == 401
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_protected_route_invalid_token(client: AsyncClient):
    """Test accessing protected route with invalid token"""
    response = await client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_refresh_token_success(client: AsyncClient, test_user_in_db: User):
    """Test successful token refresh"""
    refresh_token = create_refresh_token(test_user_in_db.id)
    response = await client.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_refresh_with_access_token(client: AsyncClient, test_user_in_db: User):
    """Test using access token for refresh (should fail)"""
    access_token = create_access_token(test_user_in_db.id)
    response = await client.post(
        "/auth/refresh",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_expired_token(client: AsyncClient, test_user_in_db: User):
    """Test using expired token"""
    expired_token = create_access_token(
        test_user_in_db.id,
        expires_delta=timedelta(minutes=-1)
    )
    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_logout(client: AsyncClient, test_user_in_db: User):
    """Test logout functionality"""
    # First get a valid token
    token = create_access_token(test_user_in_db.id)
    
    # Verify token works
    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    
    # Logout
    response = await client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    
    # Verify token no longer works
    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401 