from fastapi import APIRouter

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)

@router.get("/")
def get_inventory():
    return {
        "status": "success",
        "message": "Daftar stok",
        "data": []
    }

@router.post("/")
def add_inventory():
    return {
        "status": "success",
        "message": "Stok berhasil ditambahkan"
    }
