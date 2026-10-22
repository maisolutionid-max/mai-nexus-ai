from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.education_teacher import EducationTeacher
from app.schemas.education_teacher import (
    EducationTeacherCreate,
    EducationTeacherUpdate,
    EducationTeacherResponse,
)
from app.core.deps import get_current_user
from app.core.education_deps import get_tenant_id, require_education_permission

router = APIRouter(prefix="/education/teachers", tags=["Education Teachers"])

@router.post("/", response_model=EducationTeacherResponse, status_code=status.HTTP_201_CREATED)
def create_teacher(
    teacher_in: EducationTeacherCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:teachers:create")
    
    db_teacher = EducationTeacher(
        tenant_id=tenant_id,
        school_id=teacher_in.school_id,
        name=teacher_in.name,
        nip=teacher_in.nip,
        email=teacher_in.email,
        phone=teacher_in.phone,
        specialization=teacher_in.specialization,
    )
    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.get("/", response_model=List[EducationTeacherResponse])
def list_teachers(
    school_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:teachers:read")
    
    query = db.query(EducationTeacher).filter(EducationTeacher.tenant_id == tenant_id)
    if school_id:
        query = query.filter(EducationTeacher.school_id == school_id)
        
    return query.offset(skip).limit(limit).all()

@router.get("/{teacher_id}", response_model=EducationTeacherResponse)
def get_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:teachers:read")
    
    db_teacher = db.query(EducationTeacher).filter(
        EducationTeacher.id == teacher_id,
        EducationTeacher.tenant_id == tenant_id
    ).first()
    
    if not db_teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found or access denied."
        )
    return db_teacher

@router.put("/{teacher_id}", response_model=EducationTeacherResponse)
def update_teacher(
    teacher_id: int,
    teacher_in: EducationTeacherUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:teachers:update")
    
    db_teacher = db.query(EducationTeacher).filter(
        EducationTeacher.id == teacher_id,
        EducationTeacher.tenant_id == tenant_id
    ).first()
    
    if not db_teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found or access denied."
        )
        
    update_data = teacher_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_teacher, field, value)
        
    db.commit()
    db.refresh(db_teacher)
    return db_teacher

@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher(
    teacher_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:teachers:delete")
    
    db_teacher = db.query(EducationTeacher).filter(
        EducationTeacher.id == teacher_id,
        EducationTeacher.tenant_id == tenant_id
    ).first()
    
    if not db_teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found or access denied."
        )
        
    db.delete(db_teacher)
    db.commit()
    return None
