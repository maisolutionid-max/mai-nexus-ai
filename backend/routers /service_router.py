from fastapi import APIRouter

router = APIRouter(
    prefix="/services",
    tags=["Services"]
)

@router.get("/")
def get_services():
    return {
        "status": "success",
        "message": "Daftar layanan laundry",
        "data": []
    }

@router.post("/")
def create_service():
    return {
        "status": "success",
        "message": "Layanan berhasil ditambahkan"
    }
