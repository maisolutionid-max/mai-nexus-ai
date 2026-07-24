from fastapi import APIRouter

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

@router.get("/")
def get_payments():
    return {
        "status": "success",
        "message": "Daftar pembayaran",
        "data": []
    }

@router.post("/")
def create_payment():
    return {
        "status": "success",
        "message": "Pembayaran berhasil dibuat"
    }
