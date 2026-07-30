from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    product_code: str = Field(..., max_length=30)
    name: str = Field(..., max_length=150)
    category: str
    description: Optional[str] = None
    unit: str
    price: float = 0
    cost: float = 0
    stock: float = 0
    is_service: bool = False
    is_active: bool = True


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    product_code: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    price: Optional[float] = None
    cost: Optional[float] = None
    stock: Optional[float] = None
    is_service: Optional[bool] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
