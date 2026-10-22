from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.grading import AssessmentModel, StudentGradeModel
from app.schemas.grading import (
    AssessmentCreate,
    AssessmentResponse,
    AssessmentUpdate,
    StudentGradeCreate,
    StudentGradeResponse,
    StudentGradeUpdate,
)

router = APIRouter(prefix="/grading", tags=["Grading & Assessments"])


# --- ASSESSMENTS ENDPOINTS ---


@router.post(
    "/assessments/",
    response_model=AssessmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_assessment(payload: AssessmentCreate, db: Session = Depends(get_db)):
  new_assessment = AssessmentModel(**payload.dict())
  db.add(new_assessment)
  db.commit()
  db.refresh(new_assessment)
  return new_assessment


@router.get("/assessments/school/{school_id}", response_model=List[AssessmentResponse])
def get_assessments_by_school(school_id: int, db: Session = Depends(get_db)):
  return (
      db.query(AssessmentModel)
      .filter(AssessmentModel.school_id == school_id)
      .all()
  )


@router.get(
    "/assessments/{assessment_id}", response_model=AssessmentResponse
)
def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
  assessment = (
      db.query(AssessmentModel)
      .filter(AssessmentModel.id == assessment_id)
      .first()
  )
  if not assessment:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found"
    )
  return assessment


@router.put(
    "/assessments/{assessment_id}", response_model=AssessmentResponse
)
def update_assessment(
    assessment_id: int, payload: AssessmentUpdate, db: Session = Depends(get_db)
):
  assessment = (
      db.query(AssessmentModel)
      .filter(AssessmentModel.id == assessment_id)
      .first()
  )
  if not assessment:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found"
    )

  update_data = payload.dict(exclude_unset=True)
  for key, value in update_data.items():
    setattr(assessment, key, value)

  db.commit()
  db.refresh(assessment)
  return assessment


@router.delete("/assessments/{assessment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_assessment(assessment_id: int, db: Session = Depends(get_db)):
  assessment = (
      db.query(AssessmentModel)
      .filter(AssessmentModel.id == assessment_id)
      .first()
  )
  if not assessment:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found"
    )

  db.delete(assessment)
  db.commit()
  return None


# --- STUDENT GRADES ENDPOINTS ---


@router.post(
    "/grades/",
    response_model=StudentGradeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student_grade(
    payload: StudentGradeCreate, db: Session = Depends(get_db)
):
  assessment = (
      db.query(AssessmentModel)
      .filter(AssessmentModel.id == payload.assessment_id)
      .first()
  )
  if not assessment:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Assessment not found"
    )

  new_grade = StudentGradeModel(
      school_id=assessment.school_id,
      **payload.dict(),
  )
  db.add(new_grade)
  db.commit()
  db.refresh(new_grade)
  return new_grade


@router.get(
    "/grades/assessment/{assessment_id}",
    response_model=List[StudentGradeResponse],
)
def get_grades_by_assessment(assessment_id: int, db: Session = Depends(get_db)):
  return (
      db.query(StudentGradeModel)
      .filter(StudentGradeModel.assessment_id == assessment_id)
      .all()
  )


@router.get(
    "/grades/student/{student_id}", response_model=List[StudentGradeResponse]
)
def get_grades_by_student(student_id: int, db: Session = Depends(get_db)):
  return (
      db.query(StudentGradeModel)
      .filter(StudentGradeModel.student_id == student_id)
      .all()
  )


@router.put(
    "/grades/{grade_id}", response_model=StudentGradeResponse
)
def update_student_grade(
    grade_id: int, payload: StudentGradeUpdate, db: Session = Depends(get_db)
):
  grade = (
      db.query(StudentGradeModel)
      .filter(StudentGradeModel.id == grade_id)
      .first()
  )
  if not grade:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found"
    )

  update_data = payload.dict(exclude_unset=True)
  for key, value in update_data.items():
    setattr(grade, key, value)

  db.commit()
  db.refresh(grade)
  return grade


@router.delete("/grades/{grade_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_grade(grade_id: int, db: Session = Depends(get_db)):
  grade = (
      db.query(StudentGradeModel)
      .filter(StudentGradeModel.id == grade_id)
      .first()
  )
  if not grade:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Grade not found"
    )

  db.delete(grade)
  db.commit()
  return None
