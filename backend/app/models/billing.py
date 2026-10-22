import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from app.database import Base


class SchoolBillModel(Base):
  __tablename__ = "school_bills"

  id = Column(Integer, primary_key=True, index=True)
  school_id = Column(
      Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
  )
  student_id = Column(
      Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False
  )

  title = Column(String(255), nullable=False)  # e.g., 'SPP Bulan Januari'
  description = Column(Text, nullable=True)
  amount = Column(Float, nullable=False, default=0.0)
  due_date = Column(DateTime, nullable=True)
  status = Column(
      String(50), nullable=False, default="Unpaid"
  )  # 'Unpaid', 'Paid', 'Partial'

  created_at = Column(
      DateTime, default=datetime.datetime.utcnow, nullable=False
  )
  updated_at = Column(
      DateTime,
      default=datetime.datetime.utcnow,
      onupdate=datetime.datetime.utcnow,
      nullable=False,
  )

  payments = relationship(
      "BillPaymentModel", back_populates="bill", cascade="all, delete-orphan"
  )


class BillPaymentModel(Base):
  __tablename__ = "bill_payments"

  id = Column(Integer, primary_key=True, index=True)
  school_id = Column(
      Integer, ForeignKey("schools.id", ondelete="CASCADE"), nullable=False
  )
  bill_id = Column(
      Integer, ForeignKey("school_bills.id", ondelete="CASCADE"), nullable=False
  )

  amount_paid = Column(Float, nullable=False, default=0.0)
  payment_date = Column(
      DateTime, default=datetime.datetime.utcnow, nullable=False
  )
  payment_method = Column(
      String(50), nullable=True
  )  # 'Transfer', 'Cash', 'QRIS'
  reference_number = Column(String(100), nullable=True)
  notes = Column(Text, nullable=True)

  created_at = Column(
      DateTime, default=datetime.datetime.utcnow, nullable=False
  )
  updated_at = Column(
      DateTime,
      default=datetime.datetime.utcnow,
      onupdate=datetime.datetime.utcnow,
      nullable=False,
  )

  bill = relationship("SchoolBillModel", back_populates="payments")
  
