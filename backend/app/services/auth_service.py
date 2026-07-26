from sqlalchemy.orm import Session

from models.user import User
from schemas.auth import UserRegister, UserLogin
from utils.password import hash_password, verify_password
from utils.jwt import create_access_token


def register_user(db: Session, user: UserRegister):

    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise ValueError("Email already registered")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone=user.phone,
        password=hash_password(user.password),
        role="customer",
        is_active=True
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(db: Session, user: UserLogin):

    db_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if not db_user:
        raise ValueError("Invalid email or password")

    if not verify_password(user.password, db_user.password):
        raise ValueError("Invalid email or password")

    access_token = create_access_token(
        {
            "sub": str(db_user.id),
            "email": db_user.email,
            "role": db_user.role,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
