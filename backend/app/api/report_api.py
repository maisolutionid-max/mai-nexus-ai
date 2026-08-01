from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.report import (
    DashboardSummary,
    RevenueReport,
    CustomerReport,
    OrderReport,
    ProductReport,
    PaymentReport,
)

from app.services.report_service import (
    get_dashboard_summary,
    get_revenue_report,
    get_customer_report,
    get_order_report,
    get_product_report,
    get_payment_report,
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get(
    "/dashboard",
    response_model=DashboardSummary
)
def dashboard_summary(
    db: Session = Depends(get_db)
):
    return get_dashboard_summary(db)


@router.get(
    "/revenue",
    response_model=RevenueReport
)
def revenue_report(
    db: Session = Depends(get_db)
):
    return get_revenue_report(db)


@router.get(
    "/customer",
    response_model=CustomerReport
)
def customer_report(
    db: Session = Depends(get_db)
):
    return get_customer_report(db)


@router.get(
    "/order",
    response_model=OrderReport
)
def order_report(
    db: Session = Depends(get_db)
):
    return get_order_report(db)


@router.get(
    "/product",
    response_model=ProductReport
)
def product_report(
    db: Session = Depends(get_db)
):
    return get_product_report(db)


@router.get(
    "/payment",
    response_model=PaymentReport
)
def payment_report(
    db: Session = Depends(get_db)
):
    return get_payment_report(db)
