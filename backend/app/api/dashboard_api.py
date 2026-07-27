from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db

from services.report_service import (
    get_business_summary
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/")
def dashboard(
    db: Session = Depends(get_db)
):

    return {
        "dashboard": get_business_summary(db)
    }
