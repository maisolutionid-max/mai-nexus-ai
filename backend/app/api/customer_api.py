from fastapi import APIRouter
from app.models.customer import Customer

router = APIRouter()

customers = []

@router.get("/customers")
def get_customers():
    return customers

@router.post("/customers")
def create_customer(customer: Customer):
    customers.append(customer)
    return {
        "message": "Customer berhasil ditambahkan",
        "data": customer
    }
