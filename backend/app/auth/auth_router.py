from fastapi import APIRouter
from .auth_service import login

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login_api(username: str, password: str):
    return login(username, password)
