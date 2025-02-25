from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.services.auth import AuthService
from app.models import User

router = APIRouter()

@router.post("/login",
    response_model=dict,
    summary="User login",
    description="Authenticates a user and returns a session token or JWT for subsequent requests"
)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    auth_service = AuthService(db)
    user = auth_service.authenticate(
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    access_token = security.create_access_token(user.id)
    refresh_token = security.create_refresh_token(user.id)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout",
    response_model=dict,
    summary="User logout",
    description="Invalidates a user's authentication session"
)
def logout(
    current_user: User = Depends(deps.get_current_user),
    token: str = Depends(deps.oauth2_scheme)
) -> Any:
    auth_service = AuthService()
    auth_service.blacklist_token(token)
    return {"message": "Successfully logged out"}

@router.post("/refresh",
    response_model=dict,
    summary="Refresh token",
    description="Provides a new access token if a user's current session is about to expire"
)
def refresh_token(
    db: Session = Depends(deps.get_db),
    refresh_token: str = Depends(deps.refresh_token_scheme)
) -> Any:
    auth_service = AuthService(db)
    try:
        user_id = security.decode_refresh_token(refresh_token)
        user = auth_service.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        access_token = security.create_access_token(user.id)
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )

@router.post("/test-token", 
    response_model=dict,
    summary="Test token validity",
    description="Test if the access token is valid",
    responses={
        200: {
            "description": "Token is valid",
            "content": {
                "application/json": {
                    "example": {
                        "username": "testuser",
                        "email": "test@example.com"
                    }
                }
            }
        }
    }
)
def test_token(
    current_user = Depends(deps.get_current_user)
) -> Any:
    """
    Test access token
    """
    return {
        "username": current_user.username,
        "email": current_user.email
    } 