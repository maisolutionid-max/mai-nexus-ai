from fastapi import APIRouter

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

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(dashboard_router)
api_router.include_router(customer_router)
api_router.include_router(order_router)
api_router.include_router(payment_router)
api_router.include_router(inventory_router)
api_router.include_router(notification_router)
api_router.include_router(report_router)
api_router.include_router(ai_router)
api_router.include_router(iot_router)
api_router.include_router(health_router)
