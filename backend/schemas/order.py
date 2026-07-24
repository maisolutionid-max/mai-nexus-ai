from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class OrderBase(BaseModel):
    customer_id: int
    total_amount: float
    status: str = "Pending"


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    customer_id: Optional[int] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    order_date: datetime

    model_config = {
        "from_attributes": True
  }
