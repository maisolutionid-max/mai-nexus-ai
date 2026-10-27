
from sqlalchemy.orm import Session

from app.models.user import User as UserModel
from .Password import hash_password


def create_user(user, db: Session):
    email = user.email.strip().lower()

    existing_user = (
        db.query(UserModel)
        .filter(UserModel.email == email)
        .first()
    )

    if existing_user:
        return {"detail": "Email sudah terdaftar"}

    # Registrasi publik tidak boleh menentukan role istimewa.
    new_user = UserModel(
        full_name=user.full_name,
        email=email,
        password=hash_password(user.password),
        role="customer",
        is_active=True,
    )

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)
    except Exception:
        db.rollback()
        raise

    return {
        "message": "Registrasi berhasil",
        "user": {
            "id": new_user.id,
            "full_name": new_user.full_name,
            "email": new_user.email,
            "role": new_user.role,
        },
    }
