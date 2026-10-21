"""
MAI Nexus AI
Main Application

Author : MAI Solution Hub
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine

# Import Models (Termasuk Core & Education Models jika diperlukan untuk registrasi metadata)
from app.models.user import User
from app.models.customer import Customer
from app.models.order import Order
from app.models.payment import Payment
from app.models.inventory import Inventory
from app.models.notification import Notification
from app.models.sensor import Sensor

# Central Router & Education Routers (Jika diperlukan import eksplisit tambahan)
from app.api.router import api_router
try:
    from app.api import education_academic_year_api
except ImportError:
    education_academic_year_api = None

# Create Database Tables
Base.metadata.create_all(bind=engine)

# FastAPI Application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Central API Routes
app.include_router(api_router)

# Optional: Direct safeguard registration if academic year API is separate from central router
if education_academic_year_api and hasattr(education_academic_year_api, "router"):
    # Pastikan tidak duplikat jika sudah terdaftar di api_router
    pass


@app.get("/", tags=["System"])
def root():
    return {
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "message": "Welcome to MAI Nexus AI Backend"
    }


@app.get("/ping", tags=["System"])
def ping():
    return {
        "status": "ok"
    }
