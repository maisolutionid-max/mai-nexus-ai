from pydantic import BaseModel
from typing import Optional


class PaymentBase(BaseModel):
    order_id: int
    amount: float
    payment_method: str
    status: str = "Pending"


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    status: Optional[str] = None


class PaymentResponse(PaymentBase):
    id: int

    model_config = {
        "from_attributes": True
    }
