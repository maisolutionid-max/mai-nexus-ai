from pydantic import BaseModel

class Order(BaseModel):
    invoice_number: str
    customer_id: int
    service_id: int
    weight: float
    price: float
    status: str
    pickup_date: str
    finish_date: str
    notes: str
