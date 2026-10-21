from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EducationClassBase(BaseModel):
    name: str
    grade_level: str
    school_id: int
    academic_year_id: int
    description: Optional[str] = None

class EducationClassCreate(EducationClassBase):
    pass

class EducationClassUpdate(BaseModel):
    name: Optional[str] = None
    grade_level: Optional[str] = None
    academic_year_id: Optional[int] = None
    description: Optional[str] = None

class EducationClassResponse(EducationClassBase):
    id: int
    tenant_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
