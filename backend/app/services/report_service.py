from sqlalchemy.orm import Session

from models.customer import Customer
from models.order import Order
from models.payment import Payment
from models.inventory import Inventory


def get_business_summary(db: Session):

    return {
        "total_customers": db.query(Customer).count(),
        "total_orders": db.query(Order).count(),
        "total_payments": db.query(Payment).count(),
        "total_inventory_items": db.query(Inventory).count()
    }


def get_order_summary(db: Session):

    orders = db.query(Order).all()

    return {
        "total_orders": len(orders),
        "pending_orders": len(
            [o for o in orders if o.status == "Pending"]
        ),
        "completed_orders": len(
            [o for o in orders if o.status == "Completed"]
        )
    }
