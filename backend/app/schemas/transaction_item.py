from pydantic import BaseModel
from typing import Optional


class TransactionItemBase(BaseModel):
    product_id: int
    quantity: float
    unit_price: float
    subtotal: float


class TransactionItemCreate(TransactionItemBase):
    pass


class TransactionItemUpdate(BaseModel):
    product_id: Optional[int] = None
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    subtotal: Optional[float] = None


class TransactionItemResponse(TransactionItemBase):
    id: int

    class Config:
        from_attributes = True
