from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class TransactionBase(BaseModel):
    transaction_number: str
    customer_id: int
    subtotal: Decimal
    discount: Decimal = Decimal("0.00")
    tax: Decimal = Decimal("0.00")
    total: Decimal
    payment_status: str = "UNPAID"
    notes: Optional[str] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    subtotal: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    tax: Optional[Decimal] = None
    total: Optional[Decimal] = None
    payment_status: Optional[str] = None
    notes: Optional[str] = None


class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
