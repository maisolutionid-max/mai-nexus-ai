from fastapi import APIRouter

router = APIRouter(
    prefix="/branches",
    tags=["Branches"]
)

@router.get("/")
def get_branches():
    return {
        "status": "success",
        "message": "Daftar cabang",
        "data": []
    }

@router.post("/")
def create_branch():
    return {
        "status": "success",
        "message": "Cabang berhasil dibuat"
    }
