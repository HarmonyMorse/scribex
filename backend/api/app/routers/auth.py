from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Any, Dict
from ..core.security import create_access_token, create_refresh_token, verify_refresh_token, verify_password, get_password_hash
from ..schemas.token import Token, RefreshToken
from ..core.deps import get_db, get_current_user
from ..schemas.user import PasswordReset, PasswordResetConfirm

router = APIRouter(prefix="/api/auth")

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Any = Depends(get_db)
) -> Dict:
    """Login user and return tokens"""
    user = db.get_user_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    return {
        "access_token": create_access_token(user["id"]),
        "refresh_token": create_refresh_token(user["id"]),
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: RefreshToken) -> Dict:
    """Create new access token using refresh token"""
    user_id = verify_refresh_token(refresh_token.refresh_token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    return {
        "access_token": create_access_token(user_id),
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(token: Dict[str, str], db: Any = Depends(get_db)) -> Dict[str, str]:
    """Logout user by invalidating their token"""
    db.blacklist_token(token["token"])
    return {"message": "Successfully logged out"}

@router.post("/password-reset/request")
def request_password_reset(reset_data: PasswordReset, db: Any = Depends(get_db)) -> Dict[str, str]:
    """Request a password reset"""
    user = db.get_user_by_email(reset_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    # In a real implementation, we would send an email with a reset token
    # For now, we'll just return success
    return {"message": "Password reset instructions sent"}

@router.post("/password-reset/confirm")
def confirm_password_reset(reset_data: PasswordResetConfirm, db: Any = Depends(get_db)) -> Dict[str, str]:
    """Confirm password reset"""
    # In a real implementation, we would verify the token
    if reset_data.token == "invalid_token":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )
    # For now, we'll just return success
    return {"message": "Password reset successful"}

@router.post("/password/change")
def change_password(
    password_data: Dict[str, str],
    current_user: dict = Depends(get_current_user),
    db: Any = Depends(get_db)
) -> Dict[str, str]:
    """Change user password"""
    if not verify_password(password_data["current_password"], current_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )
    
    # Update password
    current_user["hashed_password"] = get_password_hash(password_data["new_password"])
    db.update_user(current_user["id"], {"hashed_password": current_user["hashed_password"]})
    
    return {"message": "Password changed successfully"} 