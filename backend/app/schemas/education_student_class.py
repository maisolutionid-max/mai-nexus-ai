from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EducationStudentClassBase(BaseModel):
    school_id: int
    academic_year_id: int
    class_id: int
    student_id: int
    status: Optional[str] = "active"

class EducationStudentClassCreate(EducationStudentClassBase):
    pass

class EducationStudentClassUpdate(BaseModel):
    class_id: Optional[int] = None
    status: Optional[str] = None

class EducationStudentClassResponse(EducationStudentClassBase):
    id: int
    tenant_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
      
