from pydantic import BaseModel

class LaundryOrder(BaseModel):
    customer_name: str
    service_name: str
    weight: float
    total_price: float
    status: str
