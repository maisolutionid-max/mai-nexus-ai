from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class EducationAttendance(Base):
    __tablename__ = "education_attendances"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String(50), nullable=False, index=True)
    school_id = Column(Integer, ForeignKey("education_schools.id"), nullable=False, index=True)
    class_id = Column(Integer, ForeignKey("education_classes.id"), nullable=False, index=True)
    student_id = Column(Integer, ForeignKey("education_students.id"), nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    status = Column(String(20), nullable=False) # 'present', 'sick', 'permission', 'absent'
    notes = Column(String(255), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    school = relationship("EducationSchool", backref="attendances")
    class_obj = relationship("EducationClass", backref="attendances")
    student = relationship("EducationStudent", backref="attendances")
