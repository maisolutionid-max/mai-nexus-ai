from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.order import Order
from schemas.order import OrderCreate, OrderUpdate


def get_orders(db: Session):
    return db.query(Order).all()


def get_order_by_id(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order tidak ditemukan"
        )

    return order


def create_order(db: Session, order: OrderCreate):
    new_order = Order(
        customer_id=order.customer_id,
        order_date=order.order_date,
        total_amount=order.total_amount,
        status=order.status
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


def update_order(db: Session, order_id: int, order: OrderUpdate):
    db_order = get_order_by_id(db, order_id)

    update_data = order.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)

    return db_order


def delete_order(db: Session, order_id: int):
    db_order = get_order_by_id(db, order_id)

    db.delete(db_order)
    db.commit()

    return {
        "message": "Order berhasil dihapus"
  }
