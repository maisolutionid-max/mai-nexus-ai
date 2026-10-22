import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AssessmentBase(BaseModel):
  title: str = Field(..., max_length=255)
  description: Optional[str] = None
  assessment_type: str = Field(
      ..., description="quiz, exam, assignment, project"
  )
  subject_id: int
  class_id: int
  teacher_id: Optional[int] = None
  max_score: float = 100.0
  weight: float = 1.0
  assessment_date: Optional[datetime.datetime] = None


class AssessmentCreate(AssessmentBase):
  pass


class AssessmentUpdate(BaseModel):
  title: Optional[str] = Field(None, max_length=255)
  description: Optional[str] = None
  assessment_type: Optional[str] = None
  max_score: Optional[float] = None
  weight: Optional[float] = None
  assessment_date: Optional[datetime.datetime] = None


class AssessmentResponse(AssessmentBase):
  id: int
  school_id: int
  created_at: datetime.datetime
  updated_at: datetime.datetime

  class Config:
    from_attributes = True


class StudentGradeBase(BaseModel):
  assessment_id: int
  student_id: int
  score: float
  feedback: Optional[str] = None


class StudentGradeCreate(StudentGradeBase):
  pass


class StudentGradeUpdate(BaseModel):
  score: Optional[float] = None
  feedback: Optional[str] = None


class StudentGradeResponse(StudentGradeBase):
  id: int
  school_id: int
  created_at: datetime.datetime
  updated_at: datetime.datetime

  class Config:
    from_attributes = True
