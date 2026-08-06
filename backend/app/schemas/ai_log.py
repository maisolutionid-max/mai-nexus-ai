from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class AILogBase(BaseModel):
    agent_name: str
    module: str
    user_id: Optional[int] = None
    prompt: str
    response: Optional[str] = None
    status: str = "SUCCESS"
    processing_time_ms: Optional[int] = None
    token_usage: Optional[int] = None
    model_name: Optional[str] = None
    error_message: Optional[str] = None


class AILogCreate(AILogBase):
    pass


class AILogUpdate(BaseModel):
    response: Optional[str] = None
    status: Optional[str] = None
    processing_time_ms: Optional[int] = None
    token_usage: Optional[int] = None
    model_name: Optional[str] = None
    error_message: Optional[str] = None


class AILogResponse(AILogBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
