from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class EducationStudentClass(Base):
    __tablename__ = "education_student_classes"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String(50), nullable=False, index=True)
    school_id = Column(Integer, ForeignKey("education_schools.id"), nullable=False, index=True)
    academic_year_id = Column(Integer, ForeignKey("education_academic_years.id"), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey("education_classes.id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("education_students.id"), nullable=False, index=True)
    
    status = Column(String(20), default="active", nullable=False) # active, transferred, graduated
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    school = relationship("EducationSchool")
    academic_year = relationship("EducationAcademicYear")
    class_room = relationship("EducationClass", backref="student_assignments")
    student = relationship("EducationStudent", backref="class_assignments")
