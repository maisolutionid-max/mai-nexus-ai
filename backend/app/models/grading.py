import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class AssessmentModel(Base):
  __tablename__ = "assessments"

  id = Column(Integer, primary_key=True, index=True)
  school_id = Column(
      Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
  )
  subject_id = Column(
      Integer, ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False
  )
  class_id = Column(
      Integer, ForeignKey("classes.id", ondelete="CASCADE"), nullable=False
  )
  teacher_id = Column(
      Integer, ForeignKey("teachers.id", ondelete="SET NULL"), nullable=True
  )

  title = Column(String(255), nullable=False)
  description = Column(Text, nullable=True)
  assessment_type = Column(
      String(50), nullable=False
  )  # e.g., 'quiz', 'exam', 'assignment', 'project'
  max_score = Column(Float, nullable=False, default=100.0)
  weight = Column(Float, nullable=False, default=1.0)
  assessment_date = Column(DateTime, nullable=True)

  created_at = Column(
      DateTime, default=datetime.datetime.utcnow, nullable=False
  )
  updated_at = Column(
      DateTime,
      default=datetime.datetime.utcnow,
      onupdate=datetime.datetime.utcnow,
      nullable=False,
  )

  # Relationships
  grades = relationship(
      "StudentGradeModel",
      back_populates="assessment",
      cascade="all, delete-orphan",
  )


class StudentGradeModel(Base):
  __tablename__ = "student_grades"

  id = Column(Integer, primary_key=True, index=True)
  school_id = Column(
      Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
  )
  assessment_id = Column(
      Integer, ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False
  )
  student_id = Column(
      Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False
  )

  score = Column(Float, nullable=False)
  feedback = Column(Text, nullable=True)

  created_at = Column(
      DateTime, default=datetime.datetime.utcnow, nullable=False
  )
  updated_at = Column(
      DateTime,
      default=datetime.datetime.utcnow,
      onupdate=datetime.datetime.utcnow,
      nullable=False,
  )

  # Relationships
  assessment = relationship("AssessmentModel", back_populates="grades")
