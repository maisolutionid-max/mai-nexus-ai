
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from .auth_service import login
from .user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
def login_api(
    username: str,
    password: str,
    db: Session = Depends(get_db),
):
    result = login(username, password, db)

    if "detail" in result:
        status_code = (
            403 if result["detail"] == "Akun tidak aktif"
            else 401
        )
        raise HTTPException(
            status_code=status_code,
            detail=result["detail"],
        )

    return result


@router.post("/register")
def register_api(
    user: User,
    db: Session = Depends(get_db),
):
    from .user_service import create_user

    result = create_user(user, db)

    if "detail" in result:
        raise HTTPException(
            status_code=409,
            detail=result["detail"],
        )

    return result
