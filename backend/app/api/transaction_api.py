from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionResponse
)

from app.services.transaction_service import (
    get_transactions,
    get_transaction,
    create_transaction,
    update_transaction,
    update_payment_status,
    delete_transaction,
)

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)


@router.get("/", response_model=list[TransactionResponse])
def read_transactions(db: Session = Depends(get_db)):
    return get_transactions(db)


@router.get("/{transaction_id}", response_model=TransactionResponse)
def read_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):

    transaction = get_transaction(db, transaction_id)

    if not transaction:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return transaction


@router.post("/", response_model=TransactionResponse)
def create_new_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):

    try:
        return create_transaction(db, transaction)

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.put("/{transaction_id}",
response_model=TransactionResponse)
def update_existing_transaction(
    transaction_id: int,
    transaction: TransactionUpdate,
    db: Session = Depends(get_db)
):

    updated = update_transaction(
        db,
        transaction_id,
        transaction
    )

    if not updated:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return updated


@router.patch("/{transaction_id}/payment")
def update_payment(
    transaction_id: int,
    payment_status: str,
    payment_method: str = None,
    db: Session = Depends(get_db)
):

    updated = update_payment_status(
        db,
        transaction_id,
        payment_status,
        payment_method
    )

    if not updated:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return updated


@router.delete("/{transaction_id}")
def remove_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):

    deleted = delete_transaction(
        db,
        transaction_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return {
        "message": "Transaction deleted successfully"
    }
