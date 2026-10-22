import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ReportCardBase(BaseModel):
  student_id: int
  academic_year_id: Optional[int] = None
  term: str = Field(
      ..., max_length=50, description="Semester 1, Semester 2, dll"
  )
  gpa: float = 0.0
  total_score: float = 0.0
  rank_in_class: Optional[int] = None
  teacher_notes: Optional[str] = None
  status: str = Field(
      default="Draft", description="Draft atau Published"
  )


class ReportCardCreate(ReportCardBase):
  pass


class ReportCardUpdate(BaseModel):
  term: Optional[str] = Field(None, max_length=50)
  gpa: Optional[float] = None
  total_score: Optional[float] = None
  rank_in_class: Optional[int] = None
  teacher_notes: Optional[str] = None
  status: Optional[str] = None


class ReportCardResponse(ReportCardBase):
  id: int
  school_id: int
  created_at: datetime.datetime
  updated_at: datetime.datetime

  class Config:
    from_attributes = True
