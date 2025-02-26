import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
import os
from pathlib import Path
from uuid import UUID, uuid4
from redis.asyncio import Redis
from datetime import datetime, UTC

# Set environment to testing before importing app
os.environ["ENV"] = "testing"
os.environ["ENV_FILE"] = str(Path(__file__).parent.parent / ".env.testing")

# Import all models to ensure they are registered with Base
from app.models.base import Base
from app.models.user import User
from app.models.profiles import (
    BaseProfile,
    StudentProfile,
    TeacherProfile,
    ParentProfile,
    AdminProfile,
    UserType
)

from app.main import app
from app.db.session import get_db, get_redis
from app.core.security import create_access_token, get_password_hash

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create async engine for testing
test_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
    echo=False,
)

# Create async session factory
TestingSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

@pytest_asyncio.fixture(scope="session")
async def test_engine_fixture():
    """Create the test engine"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield test_engine
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def redis():
    """Create a fake Redis instance for testing"""
    fake_redis = Redis.from_url("redis://localhost", decode_responses=True)
    return fake_redis

@pytest_asyncio.fixture(scope="function")
async def db_session(test_engine_fixture) -> AsyncSession:
    """Creates a fresh database session for each test"""
    async with TestingSessionLocal() as session:
        async with test_engine_fixture.begin() as conn:
            # Clear all tables before each test
            for table in reversed(Base.metadata.sorted_tables):
                await conn.execute(table.delete())
        yield session
        await session.rollback()
        await session.close()

@pytest_asyncio.fixture(scope="function")
async def client(db_session: AsyncSession, redis: Redis) -> AsyncClient:
    """Test client fixture that uses the db_session fixture"""
    async def override_get_db():
        yield db_session
    
    async def override_get_redis():
        return redis

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_redis] = override_get_redis
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()

@pytest.fixture
def test_user_data():
    """Provides test user data"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123!"
    }

@pytest_asyncio.fixture
async def test_user_in_db(test_user_data, db_session):
    """Creates a test user in the database"""
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

@pytest_asyncio.fixture
async def admin_token(db_session: AsyncSession):
    """Creates an admin user and returns their access token"""
    admin = User(
        id=uuid4(),
        username="admin",
        email="admin@example.com",
        hashed_password=get_password_hash("AdminPass123!"),
        is_active=True,
        created_at=datetime.now(UTC),
        updated_at=datetime.now(UTC)
    )
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    
    admin_profile = AdminProfile(
        id=uuid4(),
        user_id=admin.id,
        first_name="Admin",
        last_name="User",
        department="IT",
        user_type=UserType.ADMIN,
        type="admin"
    )
    db_session.add(admin_profile)
    await db_session.commit()
    await db_session.refresh(admin_profile)
    
    return create_access_token(admin.id)

@pytest.fixture
def student_data() -> dict:
    return {
        "username": "student1",
        "email": "student1@school.edu",
        "password": "student123",
        "profile": {
            "first_name": "Student",
            "last_name": "One",
            "grade_level": 9
        }
    }

@pytest.fixture
def teacher_data() -> dict:
    return {
        "username": "teacher1",
        "email": "teacher1@school.edu",
        "password": "teacher123",
        "profile": {
            "first_name": "Teacher",
            "last_name": "One",
            "subject": "Math",
            "room_number": "101"
        }
    } 