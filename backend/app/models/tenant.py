
"""
MAI Nexus AI Education
Tenant Model
Author: MAI Solution Hub
"""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(200),
        nullable=False,
        index=True,
    )

    slug = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default="1",
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

    schools = relationship(
        "EducationSchool",
        back_populates="tenant",
    )

    def __repr__(self):
        return (
            f"<Tenant(id={self.id}, "
            f"name={self.name!r}, "
            f"slug={self.slug!r})>"
        )
