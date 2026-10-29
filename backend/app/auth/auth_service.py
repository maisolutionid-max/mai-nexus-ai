
from sqlalchemy.orm import Session

from app.models.user import User as UserModel
from .password import verify_password
from .jwt_handler import create_access_token


def login(username: str, password: str, db: Session):
    # Untuk kompatibilitas, parameter username diisi dengan email.
    email = username.strip().lower()

    user = (
        db.query(UserModel)
        .filter(UserModel.email == email)
        .first()
    )

    if user is None or not verify_password(password, user.password):
        return {"detail": "Email atau password salah"}

    if not user.is_active:
        return {"detail": "Akun tidak aktif"}

    token = create_access_token({
        "sub": str(user.id),
        "role": user.role,
    })

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
