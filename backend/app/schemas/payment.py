from pydantic import BaseModel


class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    payment_method: str


class PaymentUpdate(BaseModel):
    amount: float | None = None
    payment_method: str | None = None
    payment_status: str | None = None


class PaymentResponse(BaseModel):
    id: int
    order_id: int
    amount: float
    payment_method: str
    payment_status: str

    class Config:
        from_attributes = True
