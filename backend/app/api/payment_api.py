from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from schemas.payment import (
    PaymentCreate,
    PaymentUpdate,
    PaymentResponse
)

from services.payment_service import (
    get_payments,
    get_payment,
    create_payment,
    update_payment,
    delete_payment
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.get("/", response_model=list[PaymentResponse])
def read_payments(
    db: Session = Depends(get_db)
):
    return get_payments(db)


@router.get("/{payment_id}", response_model=PaymentResponse)
def read_payment(
    payment_id: int,
    db: Session = Depends(get_db)
):
    payment = get_payment(
        db,
        payment_id
    )

    if not payment:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return payment


@router.post("/", response_model=PaymentResponse)
def create(
    payment: PaymentCreate,
    db: Session = Depends(get_db)
):
    return create_payment(
        db,
        payment
    )


@router.put("/{payment_id}", response_model=PaymentResponse)
def update(
    payment_id: int,
    payment: PaymentUpdate,
    db: Session = Depends(get_db)
):
    result = update_payment(
        db,
        payment_id,
        payment
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return result


@router.delete("/{payment_id}")
def delete(
    payment_id: int,
    db: Session = Depends(get_db)
):
    result = delete_payment(
        db,
        payment_id
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Payment not found"
        )

    return {
        "message": "Payment deleted successfully"
  }
