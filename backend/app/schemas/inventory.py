from pydantic import BaseModel


class InventoryCreate(BaseModel):
    item_name: str
    category: str
    stock: float
    unit: str
    minimum_stock: float


class InventoryUpdate(BaseModel):
    item_name: str | None = None
    category: str | None = None
    stock: float | None = None
    unit: str | None = None
    minimum_stock: float | None = None


class InventoryResponse(BaseModel):
    id: int
    item_name: str
    category: str
    stock: float
    unit: str
    minimum_stock: float

    class Config:
        from_attributes = True
