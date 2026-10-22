from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EducationSubjectBase(BaseModel):
    school_id: int
    name: str
    code: Optional[str] = None
    description: Optional[str] = None

class EducationSubjectCreate(EducationSubjectBase):
    pass

class EducationSubjectUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None

class EducationSubjectResponse(EducationSubjectBase):
    id: int
    tenant_id: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
