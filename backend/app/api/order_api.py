from fastapi import APIRouter
from app.models.order import Order
from app.services.pricing import calculate_price
router = APIRouter()

orders = []

@router.get("/orders")
def get_orders():
    return orders


@router.post("/orders")
def create_order(order: Order):

    order.total = calculate_price(
        order.service,
        order.weight
    )

    orders.append(order)

    return {
        "message": "Order berhasil ditambahkan",
        "data": order
    }
