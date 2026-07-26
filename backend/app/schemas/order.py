from pydantic import BaseModel


class OrderCreate(BaseModel):
    customer_id: int
    service_type: str
    weight: float
    total_price: float


class OrderUpdate(BaseModel):
    service_type: str | None = None
    weight: float | None = None
    total_price: float | None = None
    status: str | None = None


class OrderResponse(BaseModel):
    id: int
    customer_id: int
    service_type: str
    weight: float
    total_price: float
    status: str

    class Config:
        from_attributes = True
