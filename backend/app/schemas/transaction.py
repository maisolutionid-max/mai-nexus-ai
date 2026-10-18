
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal


class TransactionCreate(BaseModel):
    customer_id: int
    subtotal: Decimal = Decimal("0.00")
    discount: Decimal = Decimal("0.00")
    tax: Decimal = Decimal("0.00")
    total: Decimal
    payment_status: str = "UNPAID"
    payment_method: Optional[str] = None
    notes: Optional[str] = None


class TransactionUpdate(BaseModel):
    subtotal: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    tax: Optional[Decimal] = None
    total: Optional[Decimal] = None
    payment_status: Optional[str] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None


class TransactionResponse(BaseModel):
    id: int
    invoice_number: str
    customer_id: int
    subtotal: Decimal
    discount: Decimal
    tax: Decimal
    total_amount: Decimal
    payment_status: str
    payment_method: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
