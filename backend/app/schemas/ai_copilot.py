import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AICopilotLogBase(BaseModel):
  feature_type: str = Field(
      ..., max_length=100, description="lesson_planner, student_analytics, dll"
  )
  prompt_input: str
  ai_response: str
  teacher_id: Optional[int] = None
  student_id: Optional[int] = None


class AICopilotLogCreate(AICopilotLogBase):
  pass


class AICopilotLogResponse(AICopilotLogBase):
  id: int
  school_id: int
  created_at: datetime.datetime
  updated_at: datetime.datetime

  class Config:
    from_attributes = True
    
