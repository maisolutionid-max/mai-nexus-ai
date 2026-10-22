from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.education_subject import EducationSubject
from app.schemas.education_subject import (
    EducationSubjectCreate,
    EducationSubjectUpdate,
    EducationSubjectResponse,
)
from app.core.deps import get_current_user
from app.core.education_deps import get_tenant_id, require_education_permission

router = APIRouter(prefix="/education/subjects", tags=["Education Subjects"])

@router.post("/", response_model=EducationSubjectResponse, status_code=status.HTTP_201_CREATED)
def create_subject(
    subject_in: EducationSubjectCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:subjects:create")
    
    db_subject = EducationSubject(
        tenant_id=tenant_id,
        school_id=subject_in.school_id,
        name=subject_in.name,
        code=subject_in.code,
        description=subject_in.description,
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.get("/", response_model=List[EducationSubjectResponse])
def list_subjects(
    school_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:subjects:read")
    
    query = db.query(EducationSubject).filter(EducationSubject.tenant_id == tenant_id)
    if school_id:
        query = query.filter(EducationSubject.school_id == school_id)
        
    return query.offset(skip).limit(limit).all()

@router.get("/{subject_id}", response_model=EducationSubjectResponse)
def get_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:subjects:read")
    
    db_subject = db.query(EducationSubject).filter(
        EducationSubject.id == subject_id,
        EducationSubject.tenant_id == tenant_id
    ).first()
    
    if not db_subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found or access denied."
        )
    return db_subject

@router.put("/{subject_id}", response_model=EducationSubjectResponse)
def update_subject(
    subject_id: int,
    subject_in: EducationSubjectUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:subjects:update")
    
    db_subject = db.query(EducationSubject).filter(
        EducationSubject.id == subject_id,
        EducationSubject.tenant_id == tenant_id
    ).first()
    
    if not db_subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found or access denied."
        )
        
    update_data = subject_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_subject, field, value)
        
    db.commit()
    db.refresh(db_subject)
    return db_subject

@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:subjects:delete")
    
    db_subject = db.query(EducationSubject).filter(
        EducationSubject.id == subject_id,
        EducationSubject.tenant_id == tenant_id
    ).first()
    
    if not db_subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found or access denied."
        )
        
    db.delete(db_subject)
    db.commit()
    return None
  
