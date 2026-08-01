from datetime import datetime

from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.transaction_item import TransactionItem
from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product

from app.schemas.transaction import TransactionCreate


def get_transactions(db: Session):
    return db.query(Transaction).all()


def get_transaction(db: Session, transaction_id: int):
    return (
        db.query(Transaction)
        .filter(Transaction.id == transaction_id)
        .first()
    )


def generate_invoice_number(db: Session):

    today = datetime.now().strftime("%Y%m%d")

    last_invoice = (
        db.query(Transaction)
        .filter(
            Transaction.invoice_number.like(f"INV-{today}-%")
        )
        .order_by(Transaction.id.desc())
        .first()
    )

    if last_invoice:

        last_number = int(
            last_invoice.invoice_number.split("-")[-1]
        )

        next_number = last_number + 1

    else:

        next_number = 1

    return f"INV-{today}-{next_number:04d}"


def create_transaction(
    db: Session,
    transaction: TransactionCreate
):

    customer = (
        db.query(Customer)
        .filter(Customer.id == transaction.customer_id)
        .first()
    )

    if not customer:
        raise ValueError("Customer not found")

    if transaction.order_id:

        order = (
            db.query(Order)
            .filter(Order.id == transaction.order_id)
            .first()
        )
        from app.schemas.transaction import TransactionUpdate


def update_transaction(
    db: Session,
    transaction_id: int,
    transaction: TransactionUpdate
):

    db_transaction = get_transaction(db, transaction_id)

    if not db_transaction:
        return None

    update_data = transaction.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_transaction, key, value)

    db.commit()
    db.refresh(db_transaction)

    return db_transaction


def update_payment_status(
    db: Session,
    transaction_id: int,
    payment_status: str,
    payment_method: str = None
):

    db_transaction = get_transaction(db, transaction_id)

    if not db_transaction:
        return None

    db_transaction.payment_status = payment_status

    if payment_method:
        db_transaction.payment_method = payment_method

    db.commit()
    db.refresh(db_transaction)

    return db_transaction


def delete_transaction(
    db: Session,
    transaction_id: int
):

    db_transaction = get_transaction(db, transaction_id)

    if not db_transaction:
        return None

    db.delete(db_transaction)

    db.commit()

    return db_transaction

        if not order:
            raise ValueError("Order not found")

    subtotal = 0

    for item in transaction.items:

        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        if not product:
            raise ValueError(
                f"Product {item.product_id} not found"
            )

        subtotal += item.quantity * item.unit_price

    total = subtotal - transaction
