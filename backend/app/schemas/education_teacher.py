from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EducationTeacherBase(BaseModel):
    school_id: int
    name: str
    nip: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None

class EducationTeacherCreate(EducationTeacherBase):
    pass

class EducationTeacherUpdate(BaseModel):
    name: Optional[str] = None
    nip: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    specialization: Optional[str] = None

class EducationTeacherResponse(EducationTeacherBase):
    id: int
    tenant_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
      
