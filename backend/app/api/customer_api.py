from fastapi import APIRouter

router = APIRouter()

@router.get("/customers")
def get_customers():
    return [
        {
            "id": 1,
            "name": "Budi Santoso",
            "phone": "08123456789",
            "address": "Bandung",
            "member": True
        }
    ]
