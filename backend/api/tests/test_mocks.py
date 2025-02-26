import pytest
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.profiles import StudentProfile, TeacherProfile, ParentProfile, AdminProfile, UserType

def test_test_user_data(test_user_data):
    """Test that test_user_data fixture returns expected data"""
    assert isinstance(test_user_data, dict)
    assert "username" in test_user_data
    assert "email" in test_user_data
    assert "password" in test_user_data

@pytest.mark.asyncio
async def test_test_user_in_db(test_user_in_db: User, db_session: AsyncSession):
    """Test that test_user_in_db fixture creates a user in the database"""
    assert isinstance(test_user_in_db, User)
    assert isinstance(test_user_in_db.id, UUID)
    
    # Verify we can query the user
    result = await db_session.execute(
        select(User).filter(User.id == test_user_in_db.id)
    )
    user = result.scalar_one_or_none()
    assert user is not None
    assert user.username == test_user_in_db.username
    assert user.email == test_user_in_db.email

@pytest.mark.asyncio
async def test_admin_token(admin_token: str, db_session: AsyncSession):
    """Test that admin_token fixture creates an admin user and returns a valid token"""
    assert isinstance(admin_token, str)
    assert len(admin_token) > 0

    # First get the admin profile
    result = await db_session.execute(
        select(AdminProfile)
    )
    admin_profile = result.scalar_one_or_none()
    assert admin_profile is not None
    
    # Then verify the associated user
    result = await db_session.execute(
        select(User).where(User.id == admin_profile.user_id)
    )
    admin = result.scalar_one_or_none()
    assert admin is not None
    assert admin.is_active is True
    
    # Verify admin profile details
    assert admin_profile.user_type == UserType.ADMIN
    assert admin_profile.department == "IT" 