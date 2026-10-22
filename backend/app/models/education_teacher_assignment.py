from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class EducationTeacherAssignment(Base):
    __tablename__ = "education_teacher_assignments"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String(50), nullable=False, index=True)
    school_id = Column(Integer, ForeignKey("education_schools.id"), nullable=False, index=True)
    academic_year_id = Column(Integer, ForeignKey("education_academic_years.id"), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey("education_classes.id"), nullable=False, index=True)
    subject_id = Column(Integer, ForeignKey("education_subjects.id"), nullable=False, index=True)
    teacher_id = Column(Integer, ForeignKey("education_teachers.id"), nullable=False, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    school = relationship("EducationSchool", backref="teacher_assignments")
    academic_year = relationship("EducationAcademicYear", backref="teacher_assignments")
    class_obj = relationship("EducationClass", backref="teacher_assignments")
    subject = relationship("EducationSubject", backref="teacher_assignments")
    teacher = relationship("EducationTeacher", backref="teacher_assignments")
