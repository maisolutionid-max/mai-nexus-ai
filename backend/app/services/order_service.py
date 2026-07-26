from sqlalchemy.orm import Session

from models.order import Order
from schemas.order import OrderCreate, OrderUpdate


def get_orders(db: Session):
    return db.query(Order).all()


def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()


def create_order(db: Session, order: OrderCreate):
    db_order = Order(**order.model_dump())

    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    return db_order


def update_order(
    db: Session,
    order_id: int,
    order: OrderUpdate
):
    db_order = get_order(db, order_id)

    if not db_order:
        return None

    update_data = order.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_order, key, value)

    db.commit()
    db.refresh(db_order)

    return db_order


def delete_order(db: Session, order_id: int):
    db_order = get_order(db, order_id)

    if not db_order:
        return False

    db.delete(db_order)
    db.commit()

    return True
