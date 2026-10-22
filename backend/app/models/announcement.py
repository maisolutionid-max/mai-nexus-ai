import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from app.database import Base


class AnnouncementModel(Base):
  __tablename__ = "announcements"

  id = Column(Integer, primary_key=True, index=True)
  school_id = Column(
      Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
  )
  teacher_id = Column(
      Integer, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True
  )

  title = Column(String(255), nullable=False)
  content = Column(Text, nullable=False)
  target_role = Column(
      String(50), nullable=False, default="all"
  )  # 'all', 'teachers', 'students', 'parents'

  created_at = Column(
      DateTime, default=datetime.datetime.utcnow, nullable=False
  )
  updated_at = Column(
      DateTime,
      default=datetime.datetime.utcnow,
      onupdate=datetime.datetime.utcnow,
      nullable=False,
  )
  
