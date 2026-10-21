
"""
MAI Nexus AI Education
Education Academic Year Schemas
Author: MAI Solution Hub
"""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EducationAcademicYearBase(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    start_date: date
    end_date: date
    is_active: bool = False

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date <= self.start_date:
            raise ValueError("end_date must be after start_date")
        return self


class EducationAcademicYearCreate(EducationAcademicYearBase):
    school_id: int = Field(gt=0)


class EducationAcademicYearUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=20)
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool | None = None

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date is not None and self.end_date is not None:
            if self.end_date <= self.start_date:
                raise ValueError("end_date must be after start_date")
        return self


class EducationAcademicYearRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    tenant_id: int
    school_id: int
    name: str
    start_date: date
    end_date: date
    is_active: bool
    created_at: datetime
    updated_at: datetime
