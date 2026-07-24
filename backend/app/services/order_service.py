from app.database.database import get_connection

def get_all_orders():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")

    orders = cursor.fetchall()

    conn.close()

    return [dict(row) for row in orders]
