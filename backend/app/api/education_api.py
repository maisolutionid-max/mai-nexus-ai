
"""
MAI Nexus AI Education API
Tenant-isolated school management endpoints.

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


def get_tenant_id(current_user: dict) -> int:
    """Require a verified tenant assignment."""
    tenant_id = current_user.get("tenant_id")

    if tenant_id is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Pengguna belum ditetapkan ke tenant Education",
        )

    return int(tenant_id)


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


@router.post(
    "/schools",
    response_model=EducationSchoolResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_school(
    payload: EducationSchoolCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission("education:schools:create")
    ),
):
    tenant_id = get_tenant_id(current_user)

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

    school_data = payload.model_dump()
    school_data["tenant_id"] = tenant_id

    school = EducationSchool(**school_data)

    try:
        db.add(school)
        db.commit()
        db.refresh(school)
    except Exception:
        db.rollback()
        raise

    return school


@router.get(
    "/schools",
    response_model=list[EducationSchoolResponse],
)
def list_schools(
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission("education:schools:read")
    ),
):
    tenant_id = get_tenant_id(current_user)

    return (
        db.query(EducationSchool)
        .filter(EducationSchool.tenant_id == tenant_id)
        .order_by(EducationSchool.id.desc())
        .all()
    )


@router.get(
    "/schools/{school_id}",
    response_model=EducationSchoolResponse,
)
def get_school(
    school_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission("education:schools:read")
    ),
):
    tenant_id = get_tenant_id(current_user)

    school = (
        db.query(EducationSchool)
        .filter(
            EducationSchool.id == school_id,
            EducationSchool.tenant_id == tenant_id,
        )
        .first()
    )

    if school is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sekolah tidak ditemukan",
        )

    return school


@router.patch(
    "/schools/{school_id}",
    response_model=EducationSchoolResponse,
)
def update_school(
    school_id: int,
    payload: EducationSchoolUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission("education:schools:update")
    ),
):
    tenant_id = get_tenant_id(current_user)

    school = (
        db.query(EducationSchool)
        .filter(
            EducationSchool.id == school_id,
            EducationSchool.tenant_id == tenant_id,
        )
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

    # Never accept tenant ownership changes through the request body.
    changes.pop("tenant_id", None)

    for key, value in changes.items():
        setattr(school, key, value)

    try:
        db.commit()
        db.refresh(school)
    except Exception:
        db.rollback()
        raise

    return school


@router.delete(
    "/schools/{school_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_school(
    school_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission("education:schools:delete")
    ),
):
    tenant_id = get_tenant_id(current_user)

    school = (
        db.query(EducationSchool)
        .filter(
            EducationSchool.id == school_id,
            EducationSchool.tenant_id == tenant_id,
        )
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
