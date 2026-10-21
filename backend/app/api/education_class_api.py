from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.education_class import EducationClass
from app.schemas.education_class import (
    EducationClassCreate,
    EducationClassUpdate,
    EducationClassResponse,
)
from app.core.deps import get_current_user
from app.core.education_deps import get_tenant_id, require_education_permission

router = APIRouter(prefix="/education/classes", tags=["Education Classes"])

@router.post("/", response_model=EducationClassResponse, status_code=status.HTTP_201_CREATED)
def create_class(
    class_in: EducationClassCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    # Validasi permission
    require_education_permission(current_user, "education:classes:create")
    
    # Buat kelas baru dengan tenant_id yang terisolasi dari token pengguna
    db_class = EducationClass(
        tenant_id=tenant_id,
        school_id=class_in.school_id,
        academic_year_id=class_in.academic_year_id,
        name=class_in.name,
        grade_level=class_in.grade_level,
        description=class_in.description,
    )
    db.add(db_class)
    db.commit()
    db.refresh(db_class)
    return db_class

@router.get("/", response_model=List[EducationClassResponse])
def list_classes(
    school_id: int = None,
    academic_year_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:classes:read")
    
    query = db.query(EducationClass).filter(EducationClass.tenant_id == tenant_id)
    if school_id:
        query = query.filter(EducationClass.school_id == school_id)
    if academic_year_id:
        query = query.filter(EducationClass.academic_year_id == academic_year_id)
        
    return query.offset(skip).limit(limit).all()

@router.get("/{class_id}", response_model=EducationClassResponse)
def get_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:classes:read")
    
    db_class = db.query(EducationClass).filter(
        EducationClass.id == class_id,
        EducationClass.tenant_id == tenant_id
    ).first()
    
    if not db_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found or access denied."
        )
    return db_class

@router.put("/{class_id}", response_model=EducationClassResponse)
def update_class(
    class_id: int,
    class_in: EducationClassUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:classes:update")
    
    db_class = db.query(EducationClass).filter(
        EducationClass.id == class_id,
        EducationClass.tenant_id == tenant_id
    ).first()
    
    if not db_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found or access denied."
        )
        
    update_data = class_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_class, field, value)
        
    db.commit()
    db.refresh(db_class)
    return db_class

@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class(
    class_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:classes:delete")
    
    db_class = db.query(EducationClass).filter(
        EducationClass.id == class_id,
        EducationClass.tenant_id == tenant_id
    ).first()
    
    if not db_class:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found or access denied."
        )
        
    db.delete(db_class)
    db.commit()
    return None
