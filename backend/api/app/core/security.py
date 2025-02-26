from datetime import datetime, timedelta, UTC
from typing import Any, Union, Optional
from uuid import UUID
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from redis import Redis

from app.core.config import settings
from app.db.session import get_db, get_redis
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# In-memory token blacklist (replace with Redis in production)
token_blacklist = set()

def create_access_token(user_id: UUID, expires_delta: Optional[timedelta] = None) -> str:
    """Create access token"""
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire,
        "sub": str(user_id),
        "type": "access"
    }
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def create_refresh_token(user_id: UUID) -> str:
    """Create refresh token"""
    expire = datetime.now(UTC) + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "exp": expire,
        "sub": str(user_id),
        "type": "refresh"
    }
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)

def decode_access_token(token: str) -> UUID:
    """Decode and validate access token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != "access":
            raise ValueError("Not an access token")
        user_id = payload.get("sub")
        if user_id is None:
            raise ValueError("Token missing user ID")
        return UUID(user_id)
    except (JWTError, ValueError) as e:
        raise ValueError(str(e))

def decode_refresh_token(token: str) -> UUID:
    """Decode and validate refresh token"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        if payload.get("type") != "refresh":
            raise ValueError("Not a refresh token")
        user_id = payload.get("sub")
        if user_id is None:
            raise ValueError("Token missing user ID")
        return UUID(user_id)
    except (JWTError, ValueError) as e:
        raise ValueError(str(e))

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
    redis: Redis = Depends(get_redis)
) -> User:
    """Get current user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Check if token is blacklisted
        if await redis.get(f"blacklist:{token}"):
            raise credentials_exception

        user_id = decode_access_token(token)
        result = await db.execute(
            select(User).filter(User.id == user_id)
        )
        user = result.scalar_one_or_none()
        
        if user is None:
            raise credentials_exception
        return user
    except ValueError:
        raise credentials_exception

def blacklist_token(token: str) -> None:
    """Add a token to the blacklist"""
    token_blacklist.add(token) 