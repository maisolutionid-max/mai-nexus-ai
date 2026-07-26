from sqlalchemy.orm import Session

from models.customer import Customer
from schemas.customer import CustomerCreate, CustomerUpdate


def get_customers(db: Session):
    return db.query(Customer).all()


def get_customer(db: Session, customer_id: int):
    return (
        db.query(Customer)
        .filter(Customer.id == customer_id)
        .first()
    )


def create_customer(
    db: Session,
    customer: CustomerCreate
):
    db_customer = Customer(
        full_name=customer.full_name,
        phone=customer.phone,
        email=customer.email,
        address=customer.address,
    )

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer


def update_customer(
    db: Session,
    customer_id: int,
    customer: CustomerUpdate
):
    db_customer = get_customer(db, customer_id)

    if not db_customer:
        return None

    update_data = customer.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_customer, key, value)

    db.commit()
    db.refresh(db_customer)

    return db_customer


def delete_customer(
    db: Session,
    customer_id: int
):
    db_customer = get_customer(db, customer_id)

    if not db_customer:
        return False

    db.delete(db_customer)
    db.commit()

    return True
