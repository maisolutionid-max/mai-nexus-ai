from fastapi import APIRouter
from app.models.customer import Customer
from app.database.database import get_connection

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)

# ==========================
# GET ALL CUSTOMERS
# ==========================
@router.get("/")
def get_customers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    conn.close()

    return [dict(row) for row in customers]


# ==========================
# CREATE CUSTOMER
# ==========================
@router.post("/")
def create_customer(customer: Customer):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO customers
        (customer_code, name, phone, address)
        VALUES (?, ?, ?, ?)
        """,
        (
            customer.customer_code,
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


# ==========================
# UPDATE CUSTOMER
# ==========================
@router.put("/{customer_id}")
def update_customer(customer_id: int, customer: Customer):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE customers
        SET customer_code=?,
            name=?,
            phone=?,
            address=?
        WHERE id=?
        """,
        (
            customer.customer_code,
            customer.name,
            customer.phone,
            customer.address,
            customer_id
        )
    )

    conn.commit()
    conn.close()

    return {
        "message": "Customer berhasil diupdate"
    }


# ==========================
# DELETE CUSTOMER
# ==========================
@router.delete("/{customer_id}")
def delete_customer(customer_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM customers WHERE id=?",
        (customer_id,)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Customer berhasil dihapus"
    }
