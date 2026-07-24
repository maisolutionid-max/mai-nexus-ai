from app.database.database import get_connection


class PaymentService:

    def create_payment(self, order_id, amount, method):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO payments(
                order_id,
                amount,
                method,
                status
            )
            VALUES(?,?,?,?)
            """,
            (
                order_id,
                amount,
                method,
                "Pending"
            )
        )

        conn.commit()
        conn.close()

        return {
            "message": "Payment berhasil dibuat",
            "status": "Pending"
        }
      def paid(self, payment_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE payments
        SET status='Paid'
        WHERE id=?
        """,
        (payment_id,)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Pembayaran berhasil",
        "status": "Paid"
    }
def payment_summary(self):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        COUNT(*) AS total_payment,
        COALESCE(SUM(amount),0) AS total_amount
        FROM payments
        WHERE status='Paid'
    """)

    data = cursor.fetchone()

    conn.close()

    return {
        "total_payment": data[0],
        "total_amount": data[1]
    }
