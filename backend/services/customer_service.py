from database.Database import get_connection

def get_all_customers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers")

    data = cursor.fetchall()

    conn.close()

    return data
