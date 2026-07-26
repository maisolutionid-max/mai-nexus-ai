from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func

from database import Base


class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)

    sensor_name = Column(String(100), nullable=False)

    sensor_type = Column(String(50), nullable=False)

    location = Column(String(100), nullable=False)

    value = Column(Float, nullable=False)

    unit = Column(String(20), nullable=False)

    status = Column(String(30), default="Online")

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
