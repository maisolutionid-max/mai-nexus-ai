
"""
MAI Nexus AI Education
Education Academic Year Model
Author: MAI Solution Hub

Academic year registry scoped to a tenant and school.
"""

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.sql import func

from app.database import Base


class EducationAcademicYear(Base):
    __tablename__ = "education_academic_years"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

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

    name = Column(
        String(20),
        nullable=False,
    )

    start_date = Column(
        Date,
        nullable=False,
    )

    end_date = Column(
        Date,
        nullable=False,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default="0",
    )

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
        UniqueConstraint(
            "tenant_id",
            "school_id",
            "name",
            name="uq_education_academic_year_school_name",
        ),
        CheckConstraint(
            "end_date > start_date",
            name="ck_education_academic_year_dates",
        ),
        Index(
            "ix_education_academic_year_tenant_school",
            "tenant_id",
            "school_id",
        ),
    )

    def __repr__(self):
        return (
            f"<EducationAcademicYear("
            f"id={self.id}, "
            f"name={self.name!r}, "
            f"tenant_id={self.tenant_id}, "
            f"school_id={self.school_id}"
            f")>"
        )
