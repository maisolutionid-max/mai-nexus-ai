from fastapi import APIRouter
from app.models.order import Order

router = APIRouter()

orders = []

@router.get("/orders")
def get_orders():
    return orders

@router.post("/orders")
def create_order(order: Order):
    orders.append(order)
    return {
        "message": "Order berhasil ditambahkan",
        "data": order
    }
