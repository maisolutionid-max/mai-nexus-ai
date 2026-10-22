import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AnnouncementBase(BaseModel):
  title: str = Field(..., max_length=255)
  content: str
  target_role: str = Field(
      default="all", description="all, teachers, students, parents"
  )
  teacher_id: Optional[int] = None


class AnnouncementCreate(AnnouncementBase):
  pass


class AnnouncementUpdate(BaseModel):
  title: Optional[str] = Field(None, max_length=255)
  content: Optional[str] = None
  target_role: Optional[str] = None


class AnnouncementResponse(AnnouncementBase):
  id: int
  school_id: int
  created_at: datetime.datetime
  updated_at: datetime.datetime

  class Config:
    from_attributes = True
    
