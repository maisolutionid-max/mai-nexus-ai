
from sqlalchemy.orm import Session

from app.models.user import User as UserModel
from .Password import hash_password


ALLOWED_PUBLIC_ROLES = {"customer", "parent", "student"}


def create_user(user, db: Session):
    email = user.email.strip().lower()

    existing_user = (
        db.query(UserModel)
        .filter(UserModel.email == email)
        .first()
    )

    if existing_user:
        return {"detail": "Email sudah terdaftar"}

    requested_role = getattr(user, "role", "customer")
    role = (
        requested_role
        if requested_role in ALLOWED_PUBLIC_ROLES
        else "customer"
    )

    new_user = UserModel(
        full_name=user.full_name,
        email=email,
        password=hash_password(user.password),
        role=role,
        is_active=True,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User berhasil disimpan",
        "user": {
            "id": new_user.id,
            "full_name": new_user.full_name,
            "email": new_user.email,
            "role": new_user.role,
        },
    }
