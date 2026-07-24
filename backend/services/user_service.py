from sqlalchemy.orm import Session
from fastapi import HTTPException

from Models.user import User
from schemas.user import UserCreate, UserUpdate
from services.auth_service import get_password_hash


def get_users(db: Session):
    return db.query(User).all()


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User tidak ditemukan"
        )

    return user


def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        password=get_password_hash(user.password),
        role=user.role
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user_by_id(db, user_id)

    update_data = user.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        if key == "password":
            value = get_password_hash(value)

        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)

    db.delete(db_user)
    db.commit()

    return {
        "message": "User berhasil dihapus"
      }
