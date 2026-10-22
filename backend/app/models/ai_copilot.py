import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from app.database import Base


class AICopilotLogModel(Base):
  __tablename__ = "ai_copilot_logs"

  id = Column(Integer, primary_key=True, index=True)
  school_id = Column(
      Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
  )
  teacher_id = Column(
      Integer, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True
  )
  student_id = Column(
      Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=True
  )

  feature_type = Column(
      String(100), nullable=False
  )  # e.g., 'lesson_planner', 'student_analytics', 'grading_assistant'
  prompt_input = Column(Text, nullable=False)
  ai_response = Column(Text, nullable=False)

  created_at = Column(
      DateTime, default=datetime.datetime.utcnow, nullable=False
  )
  updated_at = Column(
      DateTime,
      default=datetime.datetime.utcnow,
      onupdate=datetime.datetime.utcnow,
      nullable=False,
  )
  
