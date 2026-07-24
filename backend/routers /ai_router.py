from fastapi import APIRouter

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.get("/analysis")
def ai_analysis():
    return {
        "status": "success",
        "message": "AI Analysis",
        "prediction": {},
        "recommendation": "Data belum tersedia."
    }

@router.get("/dashboard")
def ai_dashboard():
    return {
        "status": "success",
        "message": "AI Dashboard",
        "data": {}
    }
