from services.ai_service import AIService

ai = AIService()
from fastapi import APIRouter
from app.database.database import get_connection

router = APIRouter()

@router.get("/dashboard")
def dashboard():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM customers")
    total_customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]

    cursor.execute("SELECT COALESCE(SUM(total),0) FROM orders")
    omzet = cursor.fetchone()[0]

    conn.close()
summary = ai.business_summary()
prediction = ai.predict_revenue()
top_customers = ai.top_customers()
popular_services = ai.popular_services()
advice = ai.business_advice()
    return {
    "dashboard": summary,
    "prediction": prediction,
    "top_customers": top_customers,
    "popular_services": popular_services,
    "business_advice": advice
    }
