from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from passlib.context import CryptContext

from Models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str):
    return pwd_context.hash(password)


def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah"
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username atau password salah"
        )

    return user
