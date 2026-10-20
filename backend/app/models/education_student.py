"""
MAI Nexus AI Education
Education Student Model
Author: MAI Solution Hub
"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
)
from sqlalchemy.sql import func

from app.database import Base


class EducationStudent(Base):
    __tablename__ = "education_students"

    id = Column(Integer, primary_key=True, index=True)

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    school_id = Column(
        Integer,
        ForeignKey("education_schools.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    student_number = Column(String(50), nullable=False)
    full_name = Column(String(150), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        Index(
            "ix_education_students_tenant_school",
            "tenant_id",
            "school_id",
        ),
        Index(
            "ix_education_students_tenant_number",
            "tenant_id",
            "student_number",
            unique=True,
        ),
  )
  
