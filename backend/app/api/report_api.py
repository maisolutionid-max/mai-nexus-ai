from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from services.report_service import (
    get_business_summary,
    get_order_summary
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/summary")
def business_summary(
    db: Session = Depends(get_db)
):
    return get_business_summary(db)


@router.get("/orders")
def order_summary(
    db: Session = Depends(get_db)
):
    return get_order_summary(db)
