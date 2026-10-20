
"""
MAI Nexus AI Education API
School management endpoints with JWT authentication and RBAC.

Author: MAI Solution Hub
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.education_permissions import (
    require_education_permission,
)
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


# ============================================================
# PUBLIC ENDPOINTS
# ============================================================

@router.get("/")
def education_status():
    return {
        "module": "MAI Nexus AI Education",
        "status": "development",
        "version": "0.1.0",
    }


@router.get("/health")
def education_health():
    return {
        "module": "education",
        "status": "ok",
    }


# ============================================================
# CREATE SCHOOL
# Permission: education:schools:create
# ============================================================

@router.post(
    "/schools",
    response_model=EducationSchoolResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_school(
    payload: EducationSchoolCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission(
            "education:schools:create"
        )
    ),
):
    if payload.npsn:
        existing = (
            db.query(EducationSchool)
            .filter(EducationSchool.npsn == payload.npsn)
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="NPSN sudah terdaftar",
            )

    school = EducationSchool(**payload.model_dump())

    try:
        db.add(school)
        db.commit()
        db.refresh(school)
    except Exception:
        db.rollback()
        raise

    return school


# ============================================================
# LIST SCHOOLS
# Permission: education:schools:read
# ============================================================

@router.get(
    "/schools",
    response_model=list[EducationSchoolResponse],
)
def list_schools(
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission(
            "education:schools:read"
        )
    ),
):
    return (
        db.query(EducationSchool)
        .order_by(EducationSchool.id.desc())
        .all()
    )


# ============================================================
# GET SCHOOL DETAIL
# Permission: education:schools:read
# ============================================================

@router.get(
    "/schools/{school_id}",
    response_model=EducationSchoolResponse,
)
def get_school(
    school_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission(
            "education:schools:read"
        )
    ),
):
    school = (
        db.query(EducationSchool)
        .filter(EducationSchool.id == school_id)
        .first()
    )

    if school is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sekolah tidak ditemukan",
        )

    return school


# ============================================================
# UPDATE SCHOOL
# Permission: education:schools:update
# ============================================================

@router.patch(
    "/schools/{school_id}",
    response_model=EducationSchoolResponse,
)
def update_school(
    school_id: int,
    payload: EducationSchoolUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission(
            "education:schools:update"
        )
    ),
):
    school = (
        db.query(EducationSchool)
        .filter(EducationSchool.id == school_id)
        .first()
    )

    if school is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sekolah tidak ditemukan",
        )

    changes = payload.model_dump(exclude_unset=True)

    if changes.get("npsn"):
        existing = (
            db.query(EducationSchool)
            .filter(
                EducationSchool.npsn == changes["npsn"],
                EducationSchool.id != school_id,
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="NPSN sudah terdaftar",
            )

    for key, value in changes.items():
        setattr(school, key, value)

    try:
        db.commit()
        db.refresh(school)
    except Exception:
        db.rollback()
        raise

    return school


# ============================================================
# DELETE SCHOOL
# Permission: education:schools:delete
# ============================================================

@router.delete(
    "/schools/{school_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_school(
    school_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission(
            "education:schools:delete"
        )
    ),
):
    school = (
        db.query(EducationSchool)
        .filter(EducationSchool.id == school_id)
        .first()
    )

    if school is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sekolah tidak ditemukan",
        )

    try:
        db.delete(school)
        db.commit()
    except Exception:
        db.rollback()
        raise

    return None
