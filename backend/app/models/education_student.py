
"""
MAI Nexus AI Education
Education Student Model
Author: MAI Solution Hub

Student registry for the multi-tenant education platform.
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

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Tenant ownership.
    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # School ownership.
    school_id = Column(
        Integer,
        ForeignKey("education_schools.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    # Student identity.
    student_number = Column(
        String(50),
        nullable=False,
    )

    full_name = Column(
        String(150),
        nullable=False,
    )

    # Student status.
    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1",
    )

    # Audit timestamps.
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
        # Optimize queries filtered by tenant and school.
        Index(
            "ix_education_students_tenant_school",
            "tenant_id",
            "school_id",
        ),

        # Student numbers must be unique within each tenant.
        Index(
            "ix_education_students_tenant_number",
            "tenant_id",
            "student_number",
            unique=True,
        ),
    )

    def __repr__(self):
        return (
            f"<EducationStudent("
            f"id={self.id}, "
            f"student_number={self.student_number!r}, "
            f"full_name={self.full_name!r}, "
            f"tenant_id={self.tenant_id}, "
            f"school_id={self.school_id}"
            f")>"
        )
