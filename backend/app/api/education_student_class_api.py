from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.education_student_class import EducationStudentClass
from app.schemas.education_student_class import (
    EducationStudentClassCreate,
    EducationStudentClassUpdate,
    EducationStudentClassResponse,
)
from app.core.deps import get_current_user
from app.core.education_deps import get_tenant_id, require_education_permission

router = APIRouter(prefix="/education/student-classes", tags=["Education Student Classes"])

@router.post("/", response_model=EducationStudentClassResponse, status_code=status.HTTP_201_CREATED)
def assign_student_to_class(
    assignment_in: EducationStudentClassCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:student_classes:create")
    
    db_assignment = EducationStudentClass(
        tenant_id=tenant_id,
        school_id=assignment_in.school_id,
        academic_year_id=assignment_in.academic_year_id,
        class_id=assignment_in.class_id,
        student_id=assignment_in.student_id,
        status=assignment_in.status,
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.get("/", response_model=List[EducationStudentClassResponse])
def list_student_classes(
    school_id: Optional[int] = None,
    academic_year_id: Optional[int] = None,
    class_id: Optional[int] = None,
    student_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:student_classes:read")
    
    query = db.query(EducationStudentClass).filter(EducationStudentClass.tenant_id == tenant_id)
    if school_id:
        query = query.filter(EducationStudentClass.school_id == school_id)
    if academic_year_id:
        query = query.filter(EducationStudentClass.academic_year_id == academic_year_id)
    if class_id:
        query = query.filter(EducationStudentClass.class_id == class_id)
    if student_id:
        query = query.filter(EducationStudentClass.student_id == student_id)
        
    return query.offset(skip).limit(limit).all()

@router.get("/{assignment_id}", response_model=EducationStudentClassResponse)
def get_student_class(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:student_classes:read")
    
    db_assignment = db.query(EducationStudentClass).filter(
        EducationStudentClass.id == assignment_id,
        EducationStudentClass.tenant_id == tenant_id
    ).first()
    
    if not db_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student class assignment not found or access denied."
        )
    return db_assignment

@router.put("/{assignment_id}", response_model=EducationStudentClassResponse)
def update_student_class(
    assignment_id: int,
    assignment_in: EducationStudentClassUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:student_classes:update")
    
    db_assignment = db.query(EducationStudentClass).filter(
        EducationStudentClass.id == assignment_id,
        EducationStudentClass.tenant_id == tenant_id
    ).first()
    
    if not db_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student class assignment not found or access denied."
        )
        
    update_data = assignment_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_assignment, field, value)
        
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student_class(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:student_classes:delete")
    
    db_assignment = db.query(EducationStudentClass).filter(
        EducationStudentClass.id == assignment_id,
        EducationStudentClass.tenant_id == tenant_id
    ).first()
    
    if not db_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student class assignment not found or access denied."
        )
        
    db.delete(db_assignment)
    db.commit()
    return None
