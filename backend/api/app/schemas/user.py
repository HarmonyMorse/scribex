from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, ConfigDict

class UserBase(BaseModel):
    username: constr(min_length=3, max_length=50)
    email: EmailStr

class ProfileBase(BaseModel):
    first_name: constr(min_length=1, max_length=50)
    last_name: constr(min_length=1, max_length=50)

class StudentProfileCreate(ProfileBase):
    grade_level: int

class TeacherProfileCreate(ProfileBase):
    subject: str
    room_number: str

class UserCreateBase(UserBase):
    password: constr(min_length=8)

class StudentCreate(UserCreateBase):
    profile: StudentProfileCreate

class TeacherCreate(UserCreateBase):
    profile: TeacherProfileCreate

class UserUpdate(BaseModel):
    username: Optional[constr(min_length=3, max_length=50)] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=8)] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: UUID
    is_active: bool
    hashed_password: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True) 