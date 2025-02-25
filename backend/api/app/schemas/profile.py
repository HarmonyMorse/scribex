from pydantic import BaseModel, conint
from typing import Dict, List, Optional

class StudentProfileBase(BaseModel):
    """Base schema for student profile"""
    first_name: str
    last_name: str
    grade_level: conint(ge=1, le=12)  # Grades 1-12
    has_iep: bool
    iep_summary: Optional[str] = None
    accommodations: Optional[Dict[str, bool]] = None
    iep_goals: Optional[Dict[str, str]] = None

class TeacherProfileBase(BaseModel):
    """Base schema for teacher profile"""
    first_name: str
    last_name: str
    subject_areas: List[str]
    grade_levels: List[conint(ge=1, le=12)]

class GuardianProfileBase(BaseModel):
    """Base schema for guardian profile"""
    first_name: str
    last_name: str
    relationship: str
    student_ids: List[str] 