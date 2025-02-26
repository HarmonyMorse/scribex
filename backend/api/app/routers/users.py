from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID, uuid4
from redis import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_current_user, get_password_hash
from app.db.session import get_db, get_redis
from app.models.user import User
from app.models.profiles import AdminProfile, StudentProfile, TeacherProfile
from app.schemas.user import (
    UserUpdate,
    UserInDB,
    UserResponse,
    StudentCreate,
    TeacherCreate
)

router = APIRouter()

@router.get("/me", response_model=UserResponse)
async def read_users_me(
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Get current user information"""
    return UserResponse.model_validate(current_user)

@router.get("/{user_id}", response_model=UserResponse)
async def read_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Get user by ID (admin only)"""
    # Check if current user is admin
    result = await db.execute(
        select(AdminProfile).filter(AdminProfile.user_id == current_user.id)
    )
    admin_profile = result.scalar_one_or_none()
    if not admin_profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    result = await db.execute(
        select(User).filter(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.model_validate(user)

@router.post("/student", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_student(
    user_in: StudentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Create a new student user (admin only)"""
    # Check if current user is admin
    result = await db.execute(
        select(AdminProfile).filter(AdminProfile.user_id == current_user.id)
    )
    admin_profile = result.scalar_one_or_none()
    if not admin_profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if username or email already exists
    result = await db.execute(
        select(User).filter(User.username == user_in.username)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    result = await db.execute(
        select(User).filter(User.email == user_in.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = User(
        id=uuid4(),
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        is_active=True
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Create student profile
    student_profile = StudentProfile(
        user_id=user.id,
        first_name=user_in.profile.first_name,
        last_name=user_in.profile.last_name,
        grade_level=user_in.profile.grade_level
    )
    db.add(student_profile)
    await db.commit()
    
    return UserResponse.model_validate(user)

@router.post("/teacher", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_teacher(
    user_in: TeacherCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Create a new teacher user (admin only)"""
    # Check if current user is admin
    result = await db.execute(
        select(AdminProfile).filter(AdminProfile.user_id == current_user.id)
    )
    admin_profile = result.scalar_one_or_none()
    if not admin_profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    # Check if username or email already exists
    result = await db.execute(
        select(User).filter(User.username == user_in.username)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    result = await db.execute(
        select(User).filter(User.email == user_in.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = User(
        id=uuid4(),
        username=user_in.username,
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        is_active=True
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    # Create teacher profile
    teacher_profile = TeacherProfile(
        user_id=user.id,
        first_name=user_in.profile.first_name,
        last_name=user_in.profile.last_name,
        subject=user_in.profile.subject,
        room_number=user_in.profile.room_number
    )
    db.add(teacher_profile)
    await db.commit()
    
    return UserResponse.model_validate(user)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> UserResponse:
    """Update user information (admin only or self)"""
    # Check if current user is admin or self
    result = await db.execute(
        select(AdminProfile).filter(AdminProfile.user_id == current_user.id)
    )
    is_admin = result.scalar_one_or_none() is not None

    if not is_admin and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user"
        )

    # Get user to update
    result = await db.execute(
        select(User).filter(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update user fields
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.password is not None:
        user.hashed_password = get_password_hash(user_update.password)
    if user_update.is_active is not None:
        user.is_active = user_update.is_active

    await db.commit()
    return UserResponse.model_validate(user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete user (admin only)"""
    # Check if current user is admin
    result = await db.execute(
        select(AdminProfile).filter(AdminProfile.user_id == current_user.id)
    )
    admin_profile = result.scalar_one_or_none()

    if not admin_profile:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete users"
        )

    # Get user to delete
    result = await db.execute(
        select(User).filter(User.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    await db.delete(user)
    await db.commit()
    return None 