from fastapi import APIRouter

router = APIRouter()

@router.get("/customers")
def get_customers():
    return [
        {
            "name": "Budi",
            "phone": "08123456789"
        }
    ]
