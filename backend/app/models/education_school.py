from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from app.database import Base


class EducationSchool(Base):
    __tablename__ = "education_schools"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    npsn = Column(String(20), unique=True, nullable=True, index=True)
    school_level = Column(String(50), nullable=False)
    school_type = Column(String(50), nullable=False, default="general")
    address = Column(String(500), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )
  
