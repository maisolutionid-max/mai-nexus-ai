from fastapi import FastAPI
from app.api.customer_api import router as customer_router
from app.api.order_api import router as order_router
from app.api.dashboard_api import router as dashboard_router
app = FastAPI(
    title="MAI Nexus AI",
    version="1.0.0"
)

app.include_router(customer_router)
app.include_router(order_router)
app.include_router(dashboard_router)
@app.get("/")
def home():
    return {
        "message": "Welcome to MAI Nexus AI Laundry Module"
    }
