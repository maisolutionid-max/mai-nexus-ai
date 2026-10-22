import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from app.database import Base


class SchoolUserModel(Base):
  __tablename__ = "school_users"

  id = Column(Integer, primary_key=True, index=True)
  school_id = Column(
      Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
  )

  username = Column(String(100), unique=True, index=True, nullable=False)
  email = Column(String(255), unique=True, index=True, nullable=False)
  hashed_password = Column(String(255), nullable=False)
  full_name = Column(String(255), nullable=False)
  role = Column(
      String(50), nullable=False, default="student"
  )  # 'admin', 'teacher', 'student', 'parent'
  status = Column(
      String(50), nullable=False, default="active"
  )  # 'active', 'inactive'

  created_at = Column(
      DateTime, default=datetime.datetime.utcnow, nullable=False
  )
  updated_at = Column(
      DateTime,
      default=datetime.datetime.utcnow,
      onupdate=datetime.datetime.utcnow,
      nullable=False,
  )
  
