from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


class ServiceBase(BaseModel):
    service_code: str
    service_name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: Decimal
    estimated_duration: Optional[int] = None
    is_active: bool = True


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    service_code: Optional[str] = None
    service_name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Decimal] = None
    estimated_duration: Optional[int] = None
    is_active: Optional[bool] = None


class ServiceResponse(ServiceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
