from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/")
def get_users():
    return {
        "status": "success",
        "message": "User API MAI Nexus AI",
        "data": []
    }

@router.post("/")
def create_user():
    return {
        "status": "success",
        "message": "User berhasil dibuat"
    }
