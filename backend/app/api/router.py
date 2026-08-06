"""
MAI Nexus AI
Central API Router

Semua endpoint diregistrasikan pada file ini.
main.py hanya perlu memanggil api_router.

Author : MAI Solution Hub
"""

from fastapi import APIRouter

from app.api.auth_api import router as auth_router
from app.api.customer_api import router as customer_router
from app.api.order_api import router as order_router
from app.api.payment_api import router as payment_router
from app.api.dashboard_api import router as dashboard_router
from app.api.inventory_api import router as inventory_router
from app.api.product_api import router as product_router
from app.api.transaction_api import router as transaction_router
from app.api.notification_api import router as notification_router
from app.api.report_api import router as report_router
from app.api.ai_api import router as ai_router
from app.api.iot_api import router as iot_router
from app.api.health_api import router as health_router

api_router = APIRouter()

# Authentication
api_router.include_router(auth_router)

# Core Business
api_router.include_router(customer_router)
api_router.include_router(order_router)
api_router.include_router(payment_router)
api_router.include_router(product_router)
api_router.include_router(inventory_router)
api_router.include_router(transaction_router)

# Dashboard & Reporting
api_router.include_router(dashboard_router)
api_router.include_router(report_router)

# AI Services
api_router.include_router(ai_router)

# IoT Services
api_router.include_router(iot_router)

# Notification
api_router.include_router(notification_router)

# System
api_router.include_router(health_router)
