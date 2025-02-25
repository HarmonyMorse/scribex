from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from uuid import UUID

from ..core.config import settings
from ..core.security import verify_refresh_token
from ..services.mock_user_service import MockUserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def get_db() -> Generator:
    """Get database dependency"""
    try:
        db = MockUserService()
        yield db
    finally:
        pass  # No cleanup needed for mock service

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: MockUserService = Depends(get_db)
) -> Optional[dict]:
    """Get current user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Check if token is blacklisted
    if db.is_token_blacklisted(token):
        raise credentials_exception
    
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.get_user_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user 