from fastapi import FastAPI
from app.api.customer_api import router as customer_router

app = FastAPI(
    title="MAI Nexus AI",
    version="1.0.0"
)

app.include_router(customer_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to MAI Nexus AI Laundry Module"
    }
