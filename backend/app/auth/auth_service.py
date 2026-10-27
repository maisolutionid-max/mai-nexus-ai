
from sqlalchemy.orm import Session

from app.models.user import User
from app.database import SessionLocal
from .Password import verify_password
from .jwt_handler import create_access_token


def login(username: str, password: str):
    db: Session = SessionLocal()

    try:
        user = (
            db.query(User)
            .filter(User.email == username)
            .first()
        )

        if user is None:
            return {"detail": "Email atau password salah"}

        if not user.is_active:
            return {"detail": "Akun tidak aktif"}

        if not verify_password(password, user.password):
            return {"detail": "Email atau password salah"}

        token = create_access_token(
            {
                "sub": str(user.id),
                "role": user.role,
            }
        )

        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role,
            },
        }
    finally:
        db.close()
