from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class EducationTeacher(Base):
    __tablename__ = "education_teachers"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(String(50), nullable=False, index=True)
    school_id = Column(Integer, ForeignKey("education_schools.id"), nullable=False, index=True)
    name = Column(String(150), nullable=False)
    nip = Column(String(50), nullable=True) # Nomor Induk Pegawai / NUPTK
    email = Column(String(100), nullable=True)
    phone = Column(String(30), nullable=True)
    specialization = Column(String(100), nullable=True) # Bidang keahlian/mapel utama
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    school = relationship("EducationSchool", backref="teachers")
