from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class EducationClass(Base):
    __tablename__ = "education_classes"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String(50), nullable=False, index=True)
    school_id = Column(Integer, ForeignKey("education_schools.id"), nullable=False, index=True)
    academic_year_id = Column(Integer, ForeignKey("education_academic_years.id"), nullable=False, index=True)
    
    name = Column(String(100), nullable=False)  # Contoh: "X MIPA 1", "VII-A"
    grade_level = Column(String(20), nullable=False) # Contoh: "10", "7", "1"
    description = Column(String(255), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    school = relationship("EducationSchool", backref="classes")
    academic_year = relationship("EducationAcademicYear", backref="classes")
  
