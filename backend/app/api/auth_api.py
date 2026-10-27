
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.user_service import create_user
from app.auth.auth_service import login
from app.auth.user import User as UserCreate
from app.auth.jwt_handler import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_api(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    try:
        result = create_user(user, db)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registrasi gagal diproses.",
        )

    if isinstance(result, dict) and "detail" in result:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=result["detail"],
        )

    return result


@router.post("/login")
def login_api(
    username: str,
    password: str,
    db: Session = Depends(get_db),
):
    result = login(username, password, db)

    if isinstance(result, dict) and "detail" in result:
        message = result["detail"]
        code = (
            status.HTTP_403_FORBIDDEN
            if message == "Akun tidak aktif"
            else status.HTTP_401_UNAUTHORIZED
        )
        raise HTTPException(status_code=code, detail=message)

    return result
