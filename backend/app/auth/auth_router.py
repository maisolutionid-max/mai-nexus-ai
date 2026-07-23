from fastapi import APIRouter
from .auth_service import login, register
from .user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login_api(username: str, password: str):
    return login(username, password)

@router.post("/register")
def register_api(user: User):
    return register(user)
