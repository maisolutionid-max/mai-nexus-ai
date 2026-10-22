from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_role import SchoolUserModel
from app.schemas.user_role import (
    SchoolUserCreate,
    SchoolUserResponse,
    SchoolUserUpdate,
)

router = APIRouter(prefix="/users", tags=["School Users & RBAC"])


@router.post(
    "/school/{school_id}",
    response_model=SchoolUserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_school_user(
    school_id: int, payload: SchoolUserCreate, db: Session = Depends(get_db)
):
  # Cek duplikasi email/username
  existing = (
      db.query(SchoolUserModel)
      .filter(
          (SchoolUserModel.email == payload.email)
          | (SchoolUserModel.username == payload.username)
      )
      .first()
  )
  if existing:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Username or email already registered",
    )

  # Untuk MVP, password disimpan langsung atau di-hash (bisa disesuaikan dengan helper auth project Anda)
  new_user = SchoolUserModel(
      school_id=school_id,
      username=payload.username,
      email=payload.email,
      full_name=payload.full_name,
      role=payload.role,
      status=payload.status,
      hashed_password=payload.password
      + "_hashed",  # Placeholder hash sederhana jika belum ada auth utils
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user


@router.get("/school/{school_id}", response_model=List[SchoolUserResponse])
def get_users_by_school(school_id: int, db: Session = Depends(get_db)):
  return (
      db.query(SchoolUserModel)
      .filter(SchoolUserModel.school_id == school_id)
      .all()
  )


@router.get("/{user_id}", response_model=SchoolUserResponse)
def get_school_user(user_id: int, db: Session = Depends(get_db)):
  user = (
      db.query(SchoolUserModel).filter(SchoolUserModel.id == user_id).first()
  )
  if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )
  return user


@router.put("/{user_id}", response_model=SchoolUserResponse)
def update_school_user(
    user_id: int, payload: SchoolUserUpdate, db: Session = Depends(get_db)
):
  user = (
      db.query(SchoolUserModel).filter(SchoolUserModel.id == user_id).first()
  )
  if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )

  update_data = payload.dict(exclude_unset=True)
  if "password" in update_data:
    password = update_data.pop("password")
    update_data["hashed_password"] = password + "_hashed"

  for key, value in update_data.items():
    setattr(user, key, value)

  db.commit()
  db.refresh(user)
  return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_school_user(user_id: int, db: Session = Depends(get_db)):
  user = (
      db.query(SchoolUserModel).filter(SchoolUserModel.id == user_id).first()
  )
  if not user:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
    )

  db.delete(user)
  db.commit()
  return None
