from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EducationTeacherAssignmentBase(BaseModel):
    school_id: int
    academic_year_id: int
    class_id: int
    subject_id: int
    teacher_id: int

class EducationTeacherAssignmentCreate(EducationTeacherAssignmentBase):
    pass

class EducationTeacherAssignmentUpdate(BaseModel):
    class_id: Optional[int] = None
    subject_id: Optional[int] = None
    teacher_id: Optional[int] = None

class EducationTeacherAssignmentResponse(EducationTeacherAssignmentBase):
    id: int
    tenant_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
