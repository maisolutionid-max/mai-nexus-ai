
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from .auth_service import login
from .user import User
from .user_service import create_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/login")
def login_api(username: str, password: str, db: Session = Depends(get_db)):
    result = login(username, password, db)

    if "detail" in result:
        raise HTTPException(status_code=401, detail=result["detail"])

    return result


@router.post("/register")
def register_api(user: User, db: Session = Depends(get_db)):
    result = create_user(user, db)

    if "detail" in result:
        raise HTTPException(status_code=409, detail=result["detail"])

    return result
