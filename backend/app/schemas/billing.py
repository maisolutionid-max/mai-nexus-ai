import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SchoolBillBase(BaseModel):
  student_id: int
  title: str = Field(..., max_length=255)
  description: Optional[str] = None
  amount: float = 0.0
  due_date: Optional[datetime.datetime] = None
  status: str = Field(default="Unpaid", description="Unpaid, Paid, Partial")


class SchoolBillCreate(SchoolBillBase):
  pass


class SchoolBillUpdate(BaseModel):
  title: Optional[str] = Field(None, max_length=255)
  description: Optional[str] = None
  amount: Optional[float] = None
  due_date: Optional[datetime.datetime] = None
  status: Optional[str] = None


class SchoolBillResponse(SchoolBillBase):
  id: int
  school_id: int
  created_at: datetime.datetime
  updated_at: datetime.datetime

  class Config:
    from_attributes = True


class BillPaymentBase(BaseModel):
  bill_id: int
  amount_paid: float
  payment_date: Optional[datetime.datetime] = None
  payment_method: Optional[str] = Field(
      None, description="Transfer, Cash, QRIS"
  )
  reference_number: Optional[str] = None
  notes: Optional[str] = None


class BillPaymentCreate(BillPaymentBase):
  pass


class BillPaymentUpdate(BaseModel):
  amount_paid: Optional[float] = None
  payment_date: Optional[datetime.datetime] = None
  payment_method: Optional[str] = None
  reference_number: Optional[str] = None
  notes: Optional[str] = None


class BillPaymentResponse(BillPaymentBase):
  id: int
  school_id: int
  created_at: datetime.datetime
  updated_at: datetime.datetime

  class Config:
    from_attributes = True
