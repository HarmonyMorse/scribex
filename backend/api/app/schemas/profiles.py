from typing import Optional, Literal, Union, List
from pydantic import BaseModel, EmailStr
from datetime import datetime

class ProfileBase(BaseModel):
    first_name: str
    last_name: str

class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str

class StudentProfileCreate(ProfileBase):
    grade_level: Literal[6, 7, 8]
    has_iep: bool = False
    iep_summary: Optional[str] = None
    accommodations: Optional[dict] = None
    iep_goals: Optional[dict] = None
    last_iep_review: Optional[datetime] = None

class StudentCreate(UserBase):
    profile: StudentProfileCreate

class TeacherProfileCreate(ProfileBase):
    subject_area: str

class TeacherCreate(UserBase):
    profile: TeacherProfileCreate

class ParentProfileCreate(ProfileBase):
    student_ids: Optional[List[int]] = None

class GuardianCreate(UserBase):
    profile: ParentProfileCreate

class AdminProfileCreate(ProfileBase):
    department: Optional[str] = None

class AdminCreate(UserBase):
    profile: AdminProfileCreate 