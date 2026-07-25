from fastapi import FastAPI

from app.api.customer_api import router as customer_router
from app.api.order_api import router as order_router
from app.api.dashboard_api import router as dashboard_router
from app.auth.auth_router import router as auth_router

from database.Database import init_database

app = FastAPI(
    title="MAI Nexus AI",
    version="1.0.0"
)

init_database()

app.include_router(auth_router)
app.include_router(customer_router)
app.include_router(order_router)
app.include_router(dashboard_router)

@app.get("/")
def root():
    return {
        "status": "success",
        "application": "MAI Nexus AI",
        "version": "1.0.0"
    }
