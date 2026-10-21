
"""
MAI Nexus AI Education API
Tenant-isolated school and student management endpoints.

Author: MAI Solution Hub
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.education_permissions import (
    require_education_permission,
)
from app.models.education_school import EducationSchool
from app.models.education_student import EducationStudent
from app.schemas.education_school import (
    EducationSchoolCreate,
    EducationSchoolUpdate,
    EducationSchoolResponse,
)
from app.schemas.education_student import (
    EducationStudentCreate,
    EducationStudentUpdate,
    EducationStudentResponse,
)


router = APIRouter(
    prefix="/education",
    tags=["Education"],
)


# =========================================================
# SHARED HELPERS
# =========================================================

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
    """Return a school only if it belongs to the current tenant."""
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


def get_student_for_tenant(
    db: Session,
    student_id: int,
    tenant_id: int,
) -> EducationStudent:
    """Return a student only if it belongs to the current tenant."""
    student = (
        db.query(EducationStudent)
        .filter(
            EducationStudent.id == student_id,
            EducationStudent.tenant_id == tenant_id,
        )
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Siswa tidak ditemukan",
        )

    return student


# =========================================================
# EDUCATION STATUS
# =========================================================

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


# =========================================================
# SCHOOL MANAGEMENT
# =========================================================

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
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Data sekolah bertentangan dengan data yang sudah ada",
        )
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

    return get_school_for_tenant(db, school_id, tenant_id)


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
    school = get_school_for_tenant(db, school_id, tenant_id)

    changes = payload.model_dump(exclude_unset=True)

    # Tenant ownership cannot be changed through the request body.
    changes.pop("tenant_id", None)

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
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Perubahan sekolah bertentangan dengan data yang sudah ada",
        )
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
    school = get_school_for_tenant(db, school_id, tenant_id)

    try:
        db.delete(school)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Sekolah tidak dapat dihapus karena masih memiliki data terkait",
        )
    except Exception:
        db.rollback()
        raise

    return None


# =========================================================
# STUDENT MANAGEMENT
# =========================================================

@router.post(
    "/students",
    response_model=EducationStudentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_student(
    payload: EducationStudentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission("education:students:create")
    ),
):
    tenant_id = get_tenant_id(current_user)

    # A student can only be assigned to a school in this tenant.
    get_school_for_tenant(db, payload.school_id, tenant_id)

    duplicate = (
        db.query(EducationStudent)
        .filter(
            EducationStudent.tenant_id == tenant_id,
            EducationStudent.student_number == payload.student_number,
        )
        .first()
    )

    if duplicate:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Nomor siswa sudah terdaftar pada tenant ini",
        )

    student = EducationStudent(
        tenant_id=tenant_id,
        school_id=payload.school_id,
        student_number=payload.student_number,
        full_name=payload.full_name,
        is_active=payload.is_active,
    )

    try:
        db.add(student)
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Data siswa bertentangan dengan data yang sudah ada",
        )
    except Exception:
        db.rollback()
        raise

    return student


@router.get(
    "/students",
    response_model=list[EducationStudentResponse],
)
def list_students(
    school_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission("education:students:read")
    ),
):
    tenant_id = get_tenant_id(current_user)

    query = db.query(EducationStudent).filter(
        EducationStudent.tenant_id == tenant_id
    )

    if school_id is not None:
        get_school_for_tenant(db, school_id, tenant_id)
        query = query.filter(
            EducationStudent.school_id == school_id
        )

    return query.order_by(EducationStudent.id.desc()).all()


@router.get(
    "/students/{student_id}",
    response_model=EducationStudentResponse,
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission("education:students:read")
    ),
):
    tenant_id = get_tenant_id(current_user)

    return get_student_for_tenant(db, student_id, tenant_id)


@router.patch(
    "/students/{student_id}",
    response_model=EducationStudentResponse,
)
def update_student(
    student_id: int,
    payload: EducationStudentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission("education:students:update")
    ),
):
    tenant_id = get_tenant_id(current_user)
    student = get_student_for_tenant(db, student_id, tenant_id)

    changes = payload.model_dump(exclude_unset=True)

    if changes.get("student_number") is not None:
        duplicate = (
            db.query(EducationStudent)
            .filter(
                EducationStudent.tenant_id == tenant_id,
                EducationStudent.student_number
                == changes["student_number"],
                EducationStudent.id != student_id,
            )
            .first()
        )

        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Nomor siswa sudah terdaftar pada tenant ini",
            )

    # The update schema does not accept tenant_id or school_id.
    for key, value in changes.items():
        setattr(student, key, value)

    try:
        db.commit()
        db.refresh(student)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Perubahan siswa bertentangan dengan data yang sudah ada",
        )
    except Exception:
        db.rollback()
        raise

    return student


@router.delete(
    "/students/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_education_permission("education:students:delete")
    ),
):
    tenant_id = get_tenant_id(current_user)
    student = get_student_for_tenant(db, student_id, tenant_id)

    try:
        db.delete(student)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Siswa tidak dapat dihapus karena masih memiliki data terkait",
        )
    except Exception:
        db.rollback()
        raise

    return None
