from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from database import Base, engine

# Import Models
from models.user import User
from models.customer import Customer
from models.order import Order
from models.payment import Payment
from models.inventory import Inventory
from models.notification import Notification
from models.sensor import Sensor

# Import Routers
from api.auth_api import router as auth_router
from api.dashboard_api import router as dashboard_router
from api.customer_api import router as customer_router
from api.order_api import router as order_router
from api.payment_api import router as payment_router
from api.inventory_api import router as inventory_router
from api.notification_api import router as notification_router
from api.report_api import router as report_router
from api.ai_api import router as ai_router
from api.iot_api import router as iot_router
from api.health_api import router as health_router

# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth_router)
app.include_router(dashboard_router)
app.include_router(customer_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(inventory_router)
app.include_router(notification_router)
app.include_router(report_router)
app.include_router(ai_router)
app.include_router(iot_router)
app.include_router(health_router)


@app.get("/")
def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }
