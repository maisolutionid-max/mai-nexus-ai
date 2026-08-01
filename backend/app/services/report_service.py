from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product
from app.models.transaction import Transaction
from app.models.payment import Payment


def get_dashboard_summary(db: Session):

    total_customers = db.query(Customer).count()

    total_orders = db.query(Order).count()

    total_products = db.query(Product).count()

    total_transactions = db.query(Transaction).count()

    total_payments = db.query(Payment).count()

    total_revenue = (
        db.query(func.sum(Transaction.total_amount))
        .scalar()
        or 0
    )

    outstanding_payment = (
        db.query(func.sum(Transaction.total_amount))
        .filter(Transaction.payment_status != "PAID")
        .scalar()
        or 0
    )

    return {
        "total_customers": total_customers,
        "total_orders": total_orders,
        "total_products": total_products,
        "total_transactions": total_transactions,
        "total_payments": total_payments,
        "total_revenue": total_revenue,
        "outstanding_payment": outstanding_payment,
    }


def get_revenue_report(db: Session):

    total_revenue = (
        db.query(func.sum(Transaction.total_amount))
        .scalar()
        or 0
    )

    total_transaction = db.query(Transaction).count()

    average_transaction = (
        total_revenue / total_transaction
        if total_transaction > 0
        else 0
    )

    return {
        "total_revenue": total_revenue,
        "total_transaction": total_transaction,
        "average_transaction": average_transaction,
    }


def get_customer_report(db: Session):

    total_customers = db.query(Customer).count()

    active_customers = total_customers

    return {
        "total_customers": total_customers,
        "active_customers": active_customers,
    }


def get_order_report(db: Session):

    total_orders = db.query(Order).count()

    pending_orders = (
        db.query(Order)
        .filter(Order.status == "Pending")
        .count()
    )

    processing_orders = (
        db.query(Order)
        .filter(Order.status == "Processing")
        .count()
    )

    completed_orders = (
        db.query(Order)
        .filter(Order.status == "Completed")
        .count()
    )

    cancelled_orders = (
        db.query(Order)
        .filter(Order.status == "Cancelled")
        .count()
    )

    return {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "processing_orders": processing_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
    }


def get_product_report(db: Session):

    total_products = db.query(Product).count()

    total_services = (
        db.query(Product)
        .filter(Product.is_service == True)
        .count()
    )

    active_products = (
        db.query(Product)
        .filter(Product.is_active == True)
        .count()
    )

    inactive_products = (
        db.query(Product)
        .filter(Product.is_active == False)
        .count()
    )

    return {
        "total_products": total_products,
        "total_services": total_services,
        "active_products": active_products,
        "inactive_products": inactive_products,
    }


def get_payment_report(db: Session):

    total_payments = db.query(Payment).count()

    paid_transactions = (
        db.query(Transaction)
        .filter(Transaction.payment_status == "PAID")
        .count()
    )

    unpaid_transactions = (
        db.query(Transaction)
        .filter(Transaction.payment_status == "UNPAID")
        .count()
    )

    partial_transactions = (
        db.query(Transaction)
        .filter(Transaction.payment_status == "PARTIAL")
        .count()
    )

    return {
        "total_payments": total_payments,
        "paid_transactions": paid_transactions,
        "unpaid_transactions": unpaid_transactions,
        "partial_transactions": partial_transactions,
  }from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product
from app.models.transaction import Transaction
from app.models.payment import Payment


def get_dashboard_summary(db: Session):

    total_customers = db.query(Customer).count()

    total_orders = db.query(Order).count()

    total_products = db.query(Product).count()

    total_transactions = db.query(Transaction).count()

    total_payments = db.query(Payment).count()

    total_revenue = (
        db.query(func.sum(Transaction.total_amount))
        .scalar()
        or 0
    )

    outstanding_payment = (
        db.query(func.sum(Transaction.total_amount))
        .filter(Transaction.payment_status != "PAID")
        .scalar()
        or 0
    )

    return {
        "total_customers": total_customers,
        "total_orders": total_orders,
        "total_products": total_products,
        "total_transactions": total_transactions,
        "total_payments": total_payments,
        "total_revenue": total_revenue,
        "outstanding_payment": outstanding_payment,
    }


def get_revenue_report(db: Session):

    total_revenue = (
        db.query(func.sum(Transaction.total_amount))
        .scalar()
        or 0
    )

    total_transaction = db.query(Transaction).count()

    average_transaction = (
        total_revenue / total_transaction
        if total_transaction > 0
        else 0
    )

    return {
        "total_revenue": total_revenue,
        "total_transaction": total_transaction,
        "average_transaction": average_transaction,
    }


def get_customer_report(db: Session):

    total_customers = db.query(Customer).count()

    active_customers = total_customers

    return {
        "total_customers": total_customers,
        "active_customers": active_customers,
    }


def get_order_report(db: Session):

    total_orders = db.query(Order).count()

    pending_orders = (
        db.query(Order)
        .filter(Order.status == "Pending")
        .count()
    )

    processing_orders = (
        db.query(Order)
        .filter(Order.status == "Processing")
        .count()
    )

    completed_orders = (
        db.query(Order)
        .filter(Order.status == "Completed")
        .count()
    )

    cancelled_orders = (
        db.query(Order)
        .filter(Order.status == "Cancelled")
        .count()
    )

    return {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "processing_orders": processing_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
    }


def get_product_report(db: Session):

    total_products = db.query(Product).count()

    total_services = (
        db.query(Product)
        .filter(Product.is_service == True)
        .count()
    )

    active_products = (
        db.query(Product)
        .filter(Product.is_active == True)
        .count()
    )

    inactive_products = (
        db.query(Product)
        .filter(Product.is_active == False)
        .count()
    )

    return {
        "total_products": total_products,
        "total_services": total_services,
        "active_products": active_products,
        "inactive_products": inactive_products,
    }


def get_payment_report(db: Session):

    total_payments = db.query(Payment).count()

    paid_transactions = (
        db.query(Transaction)
        .filter(Transaction.payment_status == "PAID")
        .count()
    )

    unpaid_transactions = (
        db.query(Transaction)
        .filter(Transaction.payment_status == "UNPAID")
        .count()
    )

    partial_transactions = (
        db.query(Transaction)
        .filter(Transaction.payment_status == "PARTIAL")
        .count()
    )

    return {
        "total_payments": total_payments,
        "paid_transactions": paid_transactions,
        "unpaid_transactions": unpaid_transactions,
        "partial_transactions": partial_transactions,
  }
