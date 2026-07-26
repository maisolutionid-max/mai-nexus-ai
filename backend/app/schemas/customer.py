from pydantic import BaseModel, EmailStr
from typing import Optional


class CustomerCreate(BaseModel):
    full_name: str
    phone: str
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class CustomerUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class CustomerResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    email: Optional[EmailStr]
    address: Optional[str]

    class Config:
        from_attributes = True
