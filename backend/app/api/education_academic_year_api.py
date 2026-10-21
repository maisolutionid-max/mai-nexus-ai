
"""
MAI Nexus AI Education API
Academic year management with tenant isolation.

Author: MAI Solution Hub
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.education_permissions import require_education_permission
from app.models.education_academic_year import EducationAcademicYear
from app.models.education_school import EducationSchool
from app.schemas.education_academic_year import (
    EducationAcademicYearCreate,
    EducationAcademicYearRead,
    EducationAcademicYearUpdate,
)


router = APIRouter(
    prefix="/education/academic-years",
    tags=["Education Academic Years"],
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


def get_school_for_tenant(
    db: Session,
    school_id: int,
    tenant_id: int,
) -> EducationSchool:
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


def get_academic_year_for_tenant(
    db: Session,
    academic_year_id: int,
    tenant_id: int,
) -> EducationAcademicYear:
    academic_year = (
        db.query(EducationAcademicYear)
        .filter(
            EducationAcademicYear.id == academic_year_id,
            EducationAcademicYear.tenant_id == tenant_id,
        )
        .first()
    )

    if academic_year is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tahun ajaran tidak ditemukan",
        )

    return academic_year


@router.post(
    "",
    response_model=EducationAcademicYearRead,
    status_code=status.HTTP_201_CREATED,
)
def create_academic_year(
    payload: EducationAcademicYearCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission("education:academic_years:create")
    ),
):
    tenant_id = get_tenant_id(current_user)

    get_school_for_tenant(db, payload.school_id, tenant_id)

    academic_year = EducationAcademicYear(
        tenant_id=tenant_id,
        school_id=payload.school_id,
        name=payload.name,
        start_date=payload.start_date,
        end_date=payload.end_date,
        is_active=payload.is_active,
    )

    try:
        db.add(academic_year)
        db.commit()
        db.refresh(academic_year)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tahun ajaran sudah terdaftar atau data tidak valid",
        )

    return academic_year


@router.get(
    "",
    response_model=list[EducationAcademicYearRead],
)
def list_academic_years(
    school_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission("education:academic_years:read")
    ),
):
    tenant_id = get_tenant_id(current_user)

    query = db.query(EducationAcademicYear).filter(
        EducationAcademicYear.tenant_id == tenant_id
    )

    if school_id is not None:
        get_school_for_tenant(db, school_id, tenant_id)
        query = query.filter(
            EducationAcademicYear.school_id == school_id
        )

    return query.order_by(
        EducationAcademicYear.start_date.desc(),
        EducationAcademicYear.id.desc(),
    ).all()


@router.get(
    "/{academic_year_id}",
    response_model=EducationAcademicYearRead,
)
def get_academic_year(
    academic_year_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission("education:academic_years:read")
    ),
):
    tenant_id = get_tenant_id(current_user)

    return get_academic_year_for_tenant(
        db,
        academic_year_id,
        tenant_id,
    )


@router.patch(
    "/{academic_year_id}",
    response_model=EducationAcademicYearRead,
)
def update_academic_year(
    academic_year_id: int,
    payload: EducationAcademicYearUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission("education:academic_years:update")
    ),
):
    tenant_id = get_tenant_id(current_user)

    academic_year = get_academic_year_for_tenant(
        db,
        academic_year_id,
        tenant_id,
    )

    changes = payload.model_dump(exclude_unset=True)

    # Prevent changing ownership or moving the year to another school.
    changes.pop("tenant_id", None)
    changes.pop("school_id", None)

    for key, value in changes.items():
        setattr(academic_year, key, value)

    try:
        db.commit()
        db.refresh(academic_year)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Perubahan tahun ajaran bertentangan dengan data yang ada",
        )

    return academic_year


@router.delete(
    "/{academic_year_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_academic_year(
    academic_year_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission("education:academic_years:delete")
    ),
):
    tenant_id = get_tenant_id(current_user)

    academic_year = get_academic_year_for_tenant(
        db,
        academic_year_id,
        tenant_id,
    )

    try:
        db.delete(academic_year)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tahun ajaran tidak dapat dihapus karena masih memiliki data terkait",
        )

    return None
