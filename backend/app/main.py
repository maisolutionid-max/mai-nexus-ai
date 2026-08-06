"""
MAI Nexus AI
Main Application

Author : MAI Solution Hub
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine

# Import Models
from app.models.user import User
from app.models.customer import Customer
from app.models.order import Order
from app.models.payment import Payment
from app.models.inventory import Inventory
from app.models.notification import Notification
from app.models.sensor import Sensor

# Central Router
from app.api.router import api_router

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

# Register All API Routes
app.include_router(api_router)


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
