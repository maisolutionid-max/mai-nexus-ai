from app.database.database import get_connection


class AIService:

    def business_summary(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM customers")
        total_customers = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders = cursor.fetchone()[0]

        cursor.execute("SELECT COALESCE(SUM(total),0) FROM orders")
        total_revenue = cursor.fetchone()[0]

        conn.close()

        return {
            "total_customers": total_customers,
            "total_orders": total_orders,
            "total_revenue": total_revenue
        }
def predict_revenue(self):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COALESCE(AVG(total),0)
        FROM orders
    """)

    average = cursor.fetchone()[0]

    conn.close()

    return {
        "average_order_value": average,
        "predicted_7_days": average * 7,
        "predicted_30_days": average * 30
    }
    def popular_services(self):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT service,
               COUNT(*) AS total
        FROM orders
        GROUP BY service
        ORDER BY total DESC
    """)

    services = cursor.fetchall()

    conn.close()

    return [dict(row) for row in services]
    def top_customers(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT customer_id,
                   COUNT(*) AS jumlah_order
            FROM orders
            GROUP BY customer_id
            ORDER BY jumlah_order DESC
            LIMIT 5
        """)

        data = cursor.fetchall()

        conn.close()

        return [dict(row) for row in data]
