from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.report_card import ReportCardModel
from app.schemas.report_card import (
    ReportCardCreate,
    ReportCardResponse,
    ReportCardUpdate,
)

router = APIRouter(prefix="/report-cards", tags=["Report Cards & GPA"])


@router.post(
    "/",
    response_model=ReportCardResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_report_card(payload: ReportCardCreate, db: Session = Depends(get_db)):
  # Anda bisa menyertakan logic pencarian school_id berdasarkan student jika diperlukan,
  # namun untuk saat ini kita asumsikan school_id dikirim atau diset via payload/relasi siswa.
  # Contoh sederhana, kita set default school_id dari data student jika ada, atau pastikan payload valid.
  new_report = ReportCardModel(**payload.dict())
  db.add(new_report)
  db.commit()
  db.refresh(new_report)
  return new_report


@router.get("/school/{school_id}", response_model=List[ReportCardResponse])
def get_report_cards_by_school(school_id: int, db: Session = Depends(get_db)):
  return (
      db.query(ReportCardModel)
      .filter(ReportCardModel.school_id == school_id)
      .all()
  )


@router.get("/student/{student_id}", response_model=List[ReportCardResponse])
def get_report_cards_by_student(student_id: int, db: Session = Depends(get_db)):
  return (
      db.query(ReportCardModel)
      .filter(ReportCardModel.student_id == student_id)
      .all()
  )


@router.get("/{report_id}", response_model=ReportCardResponse)
def get_report_card(report_id: int, db: Session = Depends(get_db)):
  report = (
      db.query(ReportCardModel)
      .filter(ReportCardModel.id == report_id)
      .first()
  )
  if not report:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Report card not found"
    )
  return report


@router.put("/{report_id}", response_model=ReportCardResponse)
def update_report_card(
    report_id: int, payload: ReportCardUpdate, db: Session = Depends(get_db)
):
  report = (
      db.query(ReportCardModel)
      .filter(ReportCardModel.id == report_id)
      .first()
  )
  if not report:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Report card not found"
    )

  update_data = payload.dict(exclude_unset=True)
  for key, value in update_data.items():
    setattr(report, key, value)

  db.commit()
  db.refresh(report)
  return report


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_report_card(report_id: int, db: Session = Depends(get_db)):
  report = (
      db.query(ReportCardModel)
      .filter(ReportCardModel.id == report_id)
      .first()
  )
  if not report:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Report card not found"
    )

  db.delete(report)
  db.commit()
  return None
