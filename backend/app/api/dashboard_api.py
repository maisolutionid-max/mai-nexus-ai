from fastapi import APIRouter
from app.database.database import get_connection

router = APIRouter()

@router.get("/dashboard")
def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(total),0) FROM orders")
    omzet = cursor.fetchone()[0]

    conn.close()

    return {
        "total_customers": total_customers,
        "total_orders": total_orders,
        "omzet": omzet
    }
