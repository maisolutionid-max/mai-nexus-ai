
"""
MAI Nexus AI Education
Education Tenant User Assignment Model
Author: MAI Solution Hub
"""

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.sql import func

from app.database import Base


class EducationTenantUser(Base):
    __tablename__ = "education_tenant_users"

    id = Column(
        Integer,
        primary_key=True,
    )

    user_id = Column(
        Integer,
        nullable=False,
    )

    tenant_id = Column(
        Integer,
        ForeignKey(
            "tenants.id",
            ondelete="RESTRICT",
        ),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            name="uq_education_tenant_users_user_id",
        ),
        Index(
            "ix_education_tenant_users_tenant_id",
            "tenant_id",
        ),
    )
