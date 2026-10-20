
"""
MAI Nexus AI Education
Authentication, Active User, and Tenant Validation
Author: MAI Solution Hub
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.user import User
from app.models.education_tenant_user import EducationTenantUser
from app.models.tenant import Tenant


education_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


def get_education_current_user(
    token: str = Depends(education_oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token autentikasi tidak valid",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id = payload.get("sub")

        if not user_id:
            raise credentials_exception

        try:
            user_id = int(user_id)
        except (TypeError, ValueError):
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Akun pengguna tidak aktif",
        )

    assignment = (
        db.query(EducationTenantUser)
        .filter(EducationTenantUser.user_id == user.id)
        .first()
    )

    if assignment is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Pengguna belum ditetapkan ke tenant Education",
        )

    tenant = (
        db.query(Tenant)
        .filter(
            Tenant.id == assignment.tenant_id,
            Tenant.is_active.is_(True),
        )
        .first()
    )

    if tenant is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tenant tidak ditemukan atau tidak aktif",
        )

    return {
        "user_id": user.id,
        "role": user.role,
        "tenant_id": tenant.id,
    }
