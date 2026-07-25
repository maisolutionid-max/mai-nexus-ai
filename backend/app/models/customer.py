from pydantic import BaseModel

class Customer(BaseModel):
    name: str
    phone: str
    address: str
    member: bool = False
