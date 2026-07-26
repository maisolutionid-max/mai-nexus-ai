from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
    CustomerResponse,
)
from services.customer_service import (
    get_customers,
    get_customer,
    create_customer,
    update_customer,
    delete_customer,
)

router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


@router.get(
    "/",
    response_model=list[CustomerResponse]
)
def read_customers(
    db: Session = Depends(get_db)
):
    return get_customers(db)


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse
)
def read_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    customer = get_customer(db, customer_id)

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer


@router.post(
    "/",
    response_model=CustomerResponse
)
def create(
    customer: CustomerCreate,
    db: Session = Depends(get_db)
):
    return create_customer(db, customer)


@router.put(
    "/{customer_id}",
    response_model=CustomerResponse
)
def update(
    customer_id: int,
    customer: CustomerUpdate,
    db: Session = Depends(get_db)
):
    result = update_customer(
        db,
        customer_id,
        customer
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return result


@router.delete("/{customer_id}")
def delete(
    customer_id: int,
    db: Session = Depends(get_db)
):
    result = delete_customer(
        db,
        customer_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return {
        "message": "Customer deleted successfully"
    }
