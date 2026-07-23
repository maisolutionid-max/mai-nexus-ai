from pydantic import BaseModel

class LaundryService(BaseModel):
    name: str
    price: float
    duration: int
