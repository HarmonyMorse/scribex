from datetime import datetime
from uuid import UUID
from typing import Optional, List, Dict
from pydantic import BaseModel, EmailStr, constr, conint, Field
from .profile import StudentProfileBase, TeacherProfileBase, GuardianProfileBase

class UserBase(BaseModel):
    """Base user schema"""
    username: str
    email: EmailStr

class UserCreate(UserBase):
    """Schema for creating a user"""
    password: str
    profile: StudentProfileBase | TeacherProfileBase | GuardianProfileBase

class UserResponse(UserBase):
    """Schema for user response"""
    id: str
    user_type: str
    is_active: bool
    profile: StudentProfileBase | TeacherProfileBase | GuardianProfileBase

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None

class TokenData(BaseModel):
    username: str
    user_id: UUID
    user_type: str

class PasswordReset(BaseModel):
    email: EmailStr

class PasswordResetConfirm(BaseModel):
    token: str
    new_password: constr(min_length=8)

class PasswordChange(BaseModel):
    current_password: str
    new_password: constr(min_length=8)

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDB(UserBase):
    id: UUID
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 