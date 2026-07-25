from fastapi import APIRouter

router = APIRouter()

@router.get("/orders")
def get_orders():
    return [
        {
            "id": 1,
            "customer": "Budi Santoso",
            "service": "Cuci Kering",
            "weight": 5,
            "total": 35000,
            "status": "Diterima"
        }
    ]
