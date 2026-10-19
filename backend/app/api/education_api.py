from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.education_school import EducationSchool
from app.schemas.education_school import (
    EducationSchoolCreate,
    EducationSchoolUpdate,
    EducationSchoolResponse,
)

router = APIRouter(
    prefix="/education",
    tags=["Education"],
)


@router.get("/")
def education_status():
    return {
        "module": "MAI Nexus AI Education",
        "status": "development",
        "version": "0.1.0",
    }


@router.get("/health")
def education_health():
    return {"module": "education", "status": "ok"}


@router.post(
    "/schools",
    response_model=EducationSchoolResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_school(
    payload: EducationSchoolCreate,
    db: Session = Depends(get_db),
):
    if payload.npsn:
        existing = db.query(EducationSchool).filter(
            EducationSchool.npsn == payload.npsn
        ).first()
        if existing:
            raise HTTPException(
                status_code=409,
                detail="NPSN sudah terdaftar",
            )

    school = EducationSchool(**payload.model_dump())
    db.add(school)
    db.commit()
    db.refresh(school)
    return school


@router.get("/schools", response_model=list[EducationSchoolResponse])
def list_schools(
    db: Session = Depends(get_db),
):
    return db.query(EducationSchool).order_by(EducationSchool.id.desc()).all()


@router.get("/schools/{school_id}", response_model=EducationSchoolResponse)
def get_school(
    school_id: int,
    db: Session = Depends(get_db),
):
    school = db.query(EducationSchool).filter(
        EducationSchool.id == school_id
    ).first()
    if not school:
        raise HTTPException(status_code=404, detail="Sekolah tidak ditemukan")
    return school


@router.patch("/schools/{school_id}", response_model=EducationSchoolResponse)
def update_school(
    school_id: int,
    payload: EducationSchoolUpdate,
    db: Session = Depends(get_db),
):
    school = db.query(EducationSchool).filter(
        EducationSchool.id == school_id
    ).first()
    if not school:
        raise HTTPException(status_code=404, detail="Sekolah tidak ditemukan")

    changes = payload.model_dump(exclude_unset=True)

    if changes.get("npsn"):
        existing = db.query(EducationSchool).filter(
            EducationSchool.npsn == changes["npsn"],
            EducationSchool.id != school_id,
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="NPSN sudah terdaftar")

    for key, value in changes.items():
        setattr(school, key, value)

    db.commit()
    db.refresh(school)
    return school
