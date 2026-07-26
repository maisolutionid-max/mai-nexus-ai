from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)

    message = Column(String(500), nullable=False)

    recipient = Column(String(100), nullable=False)

    channel = Column(String(30), default="system")

    is_sent = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    sent_at = Column(
        DateTime(timezone=True),
        nullable=True
    )
