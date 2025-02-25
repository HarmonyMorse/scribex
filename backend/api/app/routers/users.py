from fastapi import APIRouter, Depends, HTTPException, status
from typing import Any
from ..core.deps import get_db, get_current_user
from ..schemas.user import UserCreate, UserResponse
from ..schemas.profile import StudentProfileBase, TeacherProfileBase, GuardianProfileBase

router = APIRouter(prefix="/api/users")

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(
    current_user: dict = Depends(get_current_user)
) -> dict:
    """Get current user profile"""
    return current_user

@router.post("/student", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    user_in: UserCreate,
    db: Any = Depends(get_db)
):
    """Create a new student user"""
    # Validate that profile is StudentProfileBase
    if not isinstance(user_in.profile, StudentProfileBase):
        raise HTTPException(
            status_code=400,
            detail="Invalid profile data for student"
        )

    # Check if user exists
    if db.get_user_by_username(user_in.username) or db.get_user_by_email(user_in.email):
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )
    
    # Create user
    user = db.create_user(
        username=user_in.username,
        email=user_in.email,
        password=user_in.password,
        user_type="student",
        profile=user_in.profile.model_dump()
    )
    
    return user

@router.post("/teacher", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_teacher(
    user_in: UserCreate,
    db: Any = Depends(get_db)
):
    """Create a new teacher user"""
    # Validate that profile is TeacherProfileBase
    if not isinstance(user_in.profile, TeacherProfileBase):
        raise HTTPException(
            status_code=400,
            detail="Invalid profile data for teacher"
        )

    # Check if user exists
    if db.get_user_by_username(user_in.username) or db.get_user_by_email(user_in.email):
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )
    
    # Create user
    user = db.create_user(
        username=user_in.username,
        email=user_in.email,
        password=user_in.password,
        user_type="teacher",
        profile=user_in.profile.model_dump()
    )
    
    return user

@router.post("/guardian", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_guardian(
    user_in: UserCreate,
    db: Any = Depends(get_db)
):
    """Create a new guardian user"""
    # Validate that profile is GuardianProfileBase
    if not isinstance(user_in.profile, GuardianProfileBase):
        raise HTTPException(
            status_code=400,
            detail="Invalid profile data for guardian"
        )

    # Check if user exists
    if db.get_user_by_username(user_in.username) or db.get_user_by_email(user_in.email):
        raise HTTPException(
            status_code=400,
            detail="Username or email already registered"
        )
    
    # Create user
    user = db.create_user(
        username=user_in.username,
        email=user_in.email,
        password=user_in.password,
        user_type="guardian",
        profile=user_in.profile.model_dump()
    )
    
    return user 