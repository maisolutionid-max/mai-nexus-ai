import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class SchoolUserBase(BaseModel):
  username: str = Field(..., max_length=100)
  email: EmailStr
  full_name: str = Field(..., max_length=255)
  role: str = Field(
      default="student", description="admin, teacher, student, parent"
  )
  status: str = Field(default="active", description="active, inactive")


class SchoolUserCreate(SchoolUserBase):
  password: str = Field(..., min_length=6)


class SchoolUserUpdate(BaseModel):
  username: Optional[str] = Field(None, max_length=100)
  email: Optional[EmailStr] = None
  full_name: Optional[str] = Field(None, max_length=255)
  role: Optional[str] = None
  status: Optional[str] = None
  password: Optional[str] = Field(None, min_length=6)


class SchoolUserResponse(SchoolUserBase):
  id: int
  school_id: int
  created_at: datetime.datetime
  updated_at: datetime.datetime

  class Config:
    from_attributes = True
