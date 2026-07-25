from fastapi import APIRouter
from app.models.order import Order
from app.services.pricing import calculate_price
from app.database.database import get_connection
router = APIRouter()

orders = []
@router.get("/orders")
def get_orders():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")

    orders = cursor.fetchall()

    conn.close()

    return [dict(row) for row in orders]

@router.post("/orders")
def create_order(order: Order):

    order.total = calculate_price(
        order.service,
        order.weight
    )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO orders(
            customer_id,
            service,
            weight,
            total,
            status
        )
        VALUES(?,?,?,?,?)
        """,
        (
            order.customer_id,
            order.service,
            order.weight,
            order.total,
            order.status
        )
    )

    conn.commit()

    conn.close()

    return {
        "message": "Order berhasil ditambahkan",
        "total": order.total
    }

    orders.append(order)

    return {
        "message": "Order berhasil ditambahkan",
        "data": order
    }
