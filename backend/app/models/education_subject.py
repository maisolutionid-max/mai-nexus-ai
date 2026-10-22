from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class EducationSubject(Base):
    __tablename__ = "education_subjects"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String(50), nullable=False, index=True)
    school_id = Column(Integer, ForeignKey("education_schools.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False) # Contoh: Matematika, Bahasa Indonesia
    code = Column(String(30), nullable=True) # Contoh: MAT-101
    description = Column(String(255), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    school = relationship("EducationSchool", backref="subjects")
  
