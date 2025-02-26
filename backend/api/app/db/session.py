from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from redis import Redis
from sqlalchemy.pool import NullPool

from app.core.config import settings

# Convert SQLite URL to async format for testing
def get_async_db_url() -> str:
    if settings.SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
        return settings.SQLALCHEMY_DATABASE_URL.replace("sqlite://", "sqlite+aiosqlite://")
    return settings.SQLALCHEMY_DATABASE_URL

# Create async engine
engine = create_async_engine(
    get_async_db_url(),
    poolclass=NullPool,
    echo=settings.DEBUG,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Create Redis client
redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    password=settings.REDIS_PASSWORD,
    decode_responses=True
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def get_redis() -> Redis:
    """Get Redis client"""
    return redis_client 