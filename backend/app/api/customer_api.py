from fastapi import APIRouter
from app.models.customer import Customer

router = APIRouter()
from app.database.database import get_connection

@router.get("/customers")
def get_customers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers")

    customers = cursor.fetchall()

    conn.close()

    return [dict(row) for row in customers]

@router.post("/customers")
def create_customer(customer: Customer):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO customers(name,phone,address) VALUES (?,?,?)",
        (
            customer.name,
            customer.phone,
            customer.address
        )
    )

    conn.commit()

    conn.close()

    return {
        "message": "Customer berhasil ditambahkan"
    }
    
