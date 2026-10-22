import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class ReportCardModel(Base):
  __tablename__ = "report_cards"

  id = Column(Integer, primary_key=True, index=True)
  school_id = Column(
      Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
  )
  student_id = Column(
      Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False
  )
  academic_year_id = Column(
      Integer, ForeignKey("academic_years.id", ondelete="SET NULL"), nullable=True
  )

  term = Column(
      String(50), nullable=False
  )  # e.g., 'Semester 1', 'Semester 2', 'Ganjil 2026'
  gpa = Column(Float, nullable=False, default=0.0)
  total_score = Column(Float, nullable=False, default=0.0)
  rank_in_class = Column(Integer, nullable=True)
  teacher_notes = Column(Text, nullable=True)
  status = Column(
      String(50), nullable=False, default="Draft"
  )  # 'Draft', 'Published'

  created_at = Column(
      DateTime, default=datetime.datetime.utcnow, nullable=False
  )
  updated_at = Column(
      DateTime,
      default=datetime.datetime.utcnow,
      onupdate=datetime.datetime.utcnow,
      nullable=False,
  )
