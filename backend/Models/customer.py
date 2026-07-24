from pydantic import BaseModel

class Customer(BaseModel):
    customer_code: str
    name: str
    phone: str
    address: str
