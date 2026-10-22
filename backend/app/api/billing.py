from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.billing import BillPaymentModel, SchoolBillModel
from app.schemas.billing import (
    BillPaymentCreate,
    BillPaymentResponse,
    BillPaymentUpdate,
    SchoolBillCreate,
    SchoolBillResponse,
    SchoolBillUpdate,
)

router = APIRouter(prefix="/billing", tags=["School Billing & Payments"])


# --- SCHOOL BILLS ENDPOINTS ---


@router.post(
    "/bills/",
    response_model=SchoolBillResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_school_bill(payload: SchoolBillCreate, db: Session = Depends(get_db)):
  new_bill = SchoolBillModel(**payload.dict())
  db.add(new_bill)
  db.commit()
  db.refresh(new_bill)
  return new_bill


@router.get("/bills/school/{school_id}", response_model=List[SchoolBillResponse])
def get_bills_by_school(school_id: int, db: Session = Depends(get_db)):
  return (
      db.query(SchoolBillModel)
      .filter(SchoolBillModel.school_id == school_id)
      .all()
  )


@router.get("/bills/student/{student_id}", response_model=List[SchoolBillResponse])
def get_bills_by_student(student_id: int, db: Session = Depends(get_db)):
  return (
      db.query(SchoolBillModel)
      .filter(SchoolBillModel.student_id == student_id)
      .all()
  )


@router.get("/bills/{bill_id}", response_model=SchoolBillResponse)
def get_school_bill(bill_id: int, db: Session = Depends(get_db)):
  bill = db.query(SchoolBillModel).filter(SchoolBillModel.id == bill_id).first()
  if not bill:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="School bill not found"
    )
  return bill


@router.put("/bills/{bill_id}", response_model=SchoolBillResponse)
def update_school_bill(
    bill_id: int, payload: SchoolBillUpdate, db: Session = Depends(get_db)
):
  bill = db.query(SchoolBillModel).filter(SchoolBillModel.id == bill_id).first()
  if not bill:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="School bill not found"
    )

  update_data = payload.dict(exclude_unset=True)
  for key, value in update_data.items():
    setattr(bill, key, value)

  db.commit()
  db.refresh(bill)
  return bill


@router.delete("/bills/{bill_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school_bill(bill_id: int, db: Session = Depends(get_db)):
  bill = db.query(SchoolBillModel).filter(SchoolBillModel.id == bill_id).first()
  if not bill:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="School bill not found"
    )

  db.delete(bill)
  db.commit()
  return None


# --- BILL PAYMENTS ENDPOINTS ---


@router.post(
    "/payments/",
    response_model=BillPaymentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_bill_payment(
    payload: BillPaymentCreate, db: Session = Depends(get_db)
):
  bill = (
      db.query(SchoolBillModel)
      .filter(SchoolBillModel.id == payload.bill_id)
      .first()
  )
  if not bill:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="School bill not found"
    )

  new_payment = BillPaymentModel(
      school_id=bill.school_id,  # Mengambil school_id otomatis dari relasi tagihan
      **payload.dict(),
  )
  db.add(new_payment)

  # Update status tagihan otomatis jika lunas atau sebagian (bisa dikustomisasi)
  db.commit()
  db.refresh(new_payment)
  return new_payment


@router.get(
    "/payments/bill/{bill_id}", response_model=List[BillPaymentResponse]
)
def get_payments_by_bill(bill_id: int, db: Session = Depends(get_db)):
  return (
      db.query(BillPaymentModel)
      .filter(BillPaymentModel.bill_id == bill_id)
      .all()
  )


@router.get("/payments/{payment_id}", response_model=BillPaymentResponse)
def get_bill_payment(payment_id: int, db: Session = Depends(get_db)):
  payment = (
      db.query(BillPaymentModel)
      .filter(BillPaymentModel.id == payment_id)
      .first()
  )
  if not payment:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Payment record not found"
    )
  return payment


@router.put("/payments/{payment_id}", response_model=BillPaymentResponse)
def update_bill_payment(
    payment_id: int, payload: BillPaymentUpdate, db: Session = Depends(get_db)
):
  payment = (
      db.query(BillPaymentModel)
      .filter(BillPaymentModel.id == payment_id)
      .first()
  )
  if not payment:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Payment record not found"
    )

  update_data = payload.dict(exclude_unset=True)
  for key, value in update_data.items():
    setattr(payment, key, value)

  db.commit()
  db.refresh(payment)
  return payment


@router.delete("/payments/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bill_payment(payment_id: int, db: Session = Depends(get_db)):
  payment = (
      db.query(BillPaymentModel)
      .filter(BillPaymentModel.id == payment_id)
      .first()
  )
  if not payment:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Payment record not found"
    )

  db.delete(payment)
  db.commit()
  return None
