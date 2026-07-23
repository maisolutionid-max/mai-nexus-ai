from fastapi import APIRouter
from app.api.order_api import orders

router = APIRouter()

@router.get("/dashboard")
def dashboard():

    total_orders = len(orders)

    total_income = sum(order.total for order in orders)

    return {
        "total_orders": total_orders,
        "total_income": total_income
    }
