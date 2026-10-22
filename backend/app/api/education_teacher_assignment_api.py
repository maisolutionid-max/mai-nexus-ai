from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.education_teacher_assignment import EducationTeacherAssignment
from app.schemas.education_teacher_assignment import (
    EducationTeacherAssignmentCreate,
    EducationTeacherAssignmentUpdate,
    EducationTeacherAssignmentResponse,
)
from app.core.deps import get_current_user
from app.core.education_deps import get_tenant_id, require_education_permission

router = APIRouter(prefix="/education/teacher-assignments", tags=["Education Teacher Assignments"])

@router.post("/", response_model=EducationTeacherAssignmentResponse, status_code=status.HTTP_201_CREATED)
def create_teacher_assignment(
    assignment_in: EducationTeacherAssignmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:teacher_assignments:create")
    
    db_assignment = EducationTeacherAssignment(
        tenant_id=tenant_id,
        school_id=assignment_in.school_id,
        academic_year_id=assignment_in.academic_year_id,
        class_id=assignment_in.class_id,
        subject_id=assignment_in.subject_id,
        teacher_id=assignment_in.teacher_id,
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.get("/", response_model=List[EducationTeacherAssignmentResponse])
def list_teacher_assignments(
    school_id: Optional[int] = None,
    academic_year_id: Optional[int] = None,
    class_id: Optional[int] = None,
    teacher_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:teacher_assignments:read")
    
    query = db.query(EducationTeacherAssignment).filter(EducationTeacherAssignment.tenant_id == tenant_id)
    if school_id:
        query = query.filter(EducationTeacherAssignment.school_id == school_id)
    if academic_year_id:
        query = query.filter(EducationTeacherAssignment.academic_year_id == academic_year_id)
    if class_id:
        query = query.filter(EducationTeacherAssignment.class_id == class_id)
    if teacher_id:
        query = query.filter(EducationTeacherAssignment.teacher_id == teacher_id)
        
    return query.offset(skip).limit(limit).all()

@router.get("/{assignment_id}", response_model=EducationTeacherAssignmentResponse)
def get_teacher_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:teacher_assignments:read")
    
    db_assignment = db.query(EducationTeacherAssignment).filter(
        EducationTeacherAssignment.id == assignment_id,
        EducationTeacherAssignment.tenant_id == tenant_id
    ).first()
    
    if not db_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher assignment not found or access denied."
        )
    return db_assignment

@router.put("/{assignment_id}", response_model=EducationTeacherAssignmentResponse)
def update_teacher_assignment(
    assignment_id: int,
    assignment_in: EducationTeacherAssignmentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:teacher_assignments:update")
    
    db_assignment = db.query(EducationTeacherAssignment).filter(
        EducationTeacherAssignment.id == assignment_id,
        EducationTeacherAssignment.tenant_id == tenant_id
    ).first()
    
    if not db_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher assignment not found or access denied."
        )
        
    update_data = assignment_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_assignment, field, value)
        
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.delete("/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_teacher_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:teacher_assignments:delete")
    
    db_assignment = db.query(EducationTeacherAssignment).filter(
        EducationTeacherAssignment.id == assignment_id,
        EducationTeacherAssignment.tenant_id == tenant_id
    ).first()
    
    if not db_assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher assignment not found or access denied."
        )
        
    db.delete(db_assignment)
    db.commit()
    return None
