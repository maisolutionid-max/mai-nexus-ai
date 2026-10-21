
"""
MAI Nexus AI Education
Education Student Schemas
Author: MAI Solution Hub
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EducationStudentBase(BaseModel):
    student_number: str = Field(
        min_length=1,
        max_length=50,
    )
    full_name: str = Field(
        min_length=1,
        max_length=150,
    )
    is_active: bool = True


class EducationStudentCreate(EducationStudentBase):
    school_id: int = Field(gt=0)


class EducationStudentUpdate(BaseModel):
    student_number: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )
    full_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )
    is_active: bool | None = None


class EducationStudentResponse(EducationStudentBase):
    id: int
    tenant_id: int
    school_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
