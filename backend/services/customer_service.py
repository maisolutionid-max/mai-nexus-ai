from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.customer import Customer
from schemas.customer import CustomerCreate, CustomerUpdate


def get_customers(db: Session):
    return db.query(Customer).all()


def get_customer_by_id(db: Session, customer_id: int):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer tidak ditemukan"
        )

    return customer


def create_customer(db: Session, customer: CustomerCreate):
    new_customer = Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        address=customer.address
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


def update_customer(
    db: Session,
    customer_id: int,
    customer: CustomerUpdate
):
    db_customer = get_customer_by_id(db, customer_id)

    update_data = customer.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)

    return db_customer


def delete_customer(db: Session, customer_id: int):
    db_customer = get_customer_by_id(db, customer_id)

    db.delete(db_customer)
    db.commit()

    return {
        "message": "Customer berhasil dihapus"
    }
