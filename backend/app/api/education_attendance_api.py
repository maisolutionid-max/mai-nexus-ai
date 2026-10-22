from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.database import get_db
from app.models.education_attendance import EducationAttendance
from app.schemas.education_attendance import (
    EducationAttendanceCreate,
    EducationAttendanceUpdate,
    EducationAttendanceResponse,
)
from app.core.deps import get_current_user
from app.core.education_deps import get_tenant_id, require_education_permission

router = APIRouter(prefix="/education/attendances", tags=["Education Attendances"])

@router.post("/", response_model=EducationAttendanceResponse, status_code=status.HTTP_201_CREATED)
def create_attendance(
    attendance_in: EducationAttendanceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:attendances:create")
    
    db_attendance = EducationAttendance(
        tenant_id=tenant_id,
        school_id=attendance_in.school_id,
        class_id=attendance_in.class_id,
        student_id=attendance_in.student_id,
        date=attendance_in.date,
        status=attendance_in.status,
        notes=attendance_in.notes,
    )
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.get("/", response_model=List[EducationAttendanceResponse])
def list_attendances(
    school_id: Optional[int] = None,
    class_id: Optional[int] = None,
    student_id: Optional[int] = None,
    attendance_date: Optional[date] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:attendances:read")
    
    query = db.query(EducationAttendance).filter(EducationAttendance.tenant_id == tenant_id)
    if school_id:
        query = query.filter(EducationAttendance.school_id == school_id)
    if class_id:
        query = query.filter(EducationAttendance.class_id == class_id)
    if student_id:
        query = query.filter(EducationAttendance.student_id == student_id)
    if attendance_date:
        query = query.filter(EducationAttendance.date == attendance_date)
        
    return query.offset(skip).limit(limit).all()

@router.get("/{attendance_id}", response_model=EducationAttendanceResponse)
def get_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:attendances:read")
    
    db_attendance = db.query(EducationAttendance).filter(
        EducationAttendance.id == attendance_id,
        EducationAttendance.tenant_id == tenant_id
    ).first()
    
    if not db_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found or access denied."
        )
    return db_attendance

@router.put("/{attendance_id}", response_model=EducationAttendanceResponse)
def update_attendance(
    attendance_id: int,
    attendance_in: EducationAttendanceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:attendances:update")
    
    db_attendance = db.query(EducationAttendance).filter(
        EducationAttendance.id == attendance_id,
        EducationAttendance.tenant_id == tenant_id
    ).first()
    
    if not db_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found or access denied."
        )
        
    update_data = attendance_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_attendance, field, value)
        
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    tenant_id: str = Depends(get_tenant_id),
):
    require_education_permission(current_user, "education:attendances:delete")
    
    db_attendance = db.query(EducationAttendance).filter(
        EducationAttendance.id == attendance_id,
        EducationAttendance.tenant_id == tenant_id
    ).first()
    
    if not db_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found or access denied."
        )
        
    db.delete(db_attendance)
    db.commit()
    return None
