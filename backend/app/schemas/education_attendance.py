from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class EducationAttendanceBase(BaseModel):
    school_id: int
    class_id: int
    student_id: int
    date: date
    status: str # 'present', 'sick', 'permission', 'absent'
    notes: Optional[str] = None

class EducationAttendanceCreate(EducationAttendanceBase):
    pass

class EducationAttendanceUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[str] = None

class EducationAttendanceResponse(EducationAttendanceBase):
    id: int
    tenant_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
