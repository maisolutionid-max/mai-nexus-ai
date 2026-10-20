
"""
MAI Nexus AI Education
Education School Model
Author: MAI Solution Hub

School registry for the multi-tenant education platform.
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


class EducationSchool(Base):
    __tablename__ = "education_schools"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Tenant ownership.
    # Nullable initially to preserve compatibility with existing records.
    # Enforce tenant ownership after migrating existing data.
    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id", ondelete="RESTRICT"),
        nullable=True,
        index=True,
    )

    name = Column(
        String(200),
        nullable=False,
        index=True,
    )

    npsn = Column(
        String(20),
        unique=True,
        nullable=True,
        index=True,
    )

    school_level = Column(
        String(50),
        nullable=False,
    )

    school_type = Column(
        String(50),
        nullable=False,
        default="general",
        server_default="general",
    )

    address = Column(
        String(500),
        nullable=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1",
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now(),
        onupdate=func.now(),
    )

    __table_args__ = (
        Index(
            "ix_education_schools_tenant_active",
            "tenant_id",
            "is_active",
        ),
    )

    def __repr__(self):
        return (
            f"<EducationSchool("
            f"id={self.id}, "
            f"name={self.name!r}, "
            f"tenant_id={self.tenant_id}"
            f")>"
        )
