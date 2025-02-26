import pytest
import pytest_asyncio
from httpx import AsyncClient
from uuid import uuid4
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.main import app
from app.models.user import User
from app.models.profiles import StudentProfile, TeacherProfile, ParentProfile, AdminProfile
from app.core.security import create_access_token

@pytest.mark.asyncio
async def test_create_student(client: AsyncClient, admin_token: str, student_data: dict):
    response = await client.post(
        "/users/student",
        json=student_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == student_data["email"]

@pytest.mark.asyncio
async def test_create_teacher(client: AsyncClient, admin_token: str, teacher_data: dict):
    response = await client.post(
        "/users/teacher",
        json=teacher_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == teacher_data["email"]

@pytest.mark.asyncio
async def test_get_user_profile(client: AsyncClient, admin_token: str, db_session: AsyncSession):
    # Create a test user
    user_id = uuid4()
    user = User(
        id=user_id,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed",
        is_active=True
    )
    db_session.add(user)

    # Add profile
    profile = StudentProfile(
        user_id=user_id,
        first_name="Test",
        last_name="User",
        grade_level=6
    )
    db_session.add(profile)
    await db_session.commit()

    response = await client.get(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

@pytest.mark.asyncio
async def test_update_user_profile(client: AsyncClient, admin_token: str, db_session: AsyncSession):
    # Create a test user
    user_id = uuid4()
    user = User(
        id=user_id,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed",
        is_active=True
    )
    db_session.add(user)

    # Add profile
    profile = StudentProfile(
        user_id=user_id,
        first_name="Test",
        last_name="User",
        grade_level=6
    )
    db_session.add(profile)
    await db_session.commit()

    update_data = {
        "email": "new.email@school.edu",
        "profile": {
            "first_name": "Updated",
            "grade_level": 7
        }
    }

    response = await client.put(
        f"/users/{user_id}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "new.email@school.edu"

@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, admin_token: str, db_session: AsyncSession):
    # Create a test user
    user_id = uuid4()
    user = User(
        id=user_id,
        username="testuser",
        email="test@example.com",
        hashed_password="hashed",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()

    response = await client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 204

    # Verify user is deleted
    result = await db_session.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    assert user is None

@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    response = await client.get("/users/me")
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_invalid_token(client: AsyncClient):
    response = await client.get(
        "/users/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_read_users_me(client: AsyncClient, test_user_in_db: User):
    token = create_access_token(test_user_in_db.id)
    response = await client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == test_user_in_db.email

@pytest.mark.asyncio
async def test_read_user_by_id(client: AsyncClient, admin_token: str, test_user_in_db: User):
    response = await client.get(
        f"/users/{test_user_in_db.id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == test_user_in_db.email

@pytest.mark.asyncio
async def test_read_user_not_found(client: AsyncClient, admin_token: str):
    non_existent_id = uuid4()
    response = await client.get(
        f"/users/{non_existent_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_read_user_unauthorized(client: AsyncClient, test_user_in_db: User):
    token = create_access_token(test_user_in_db.id)
    response = await client.get(
        f"/users/{test_user_in_db.id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403

@pytest.mark.asyncio
async def test_update_user(client: AsyncClient, admin_token: str, test_user_in_db: User):
    update_data = {
        "email": "updated@example.com"
    }
    response = await client.put(
        f"/users/{test_user_in_db.id}",
        json=update_data,
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "updated@example.com" 