from .auth_api import router as auth_router
from .dashboard_api import router as dashboard_router
from .customer_api import router as customer_router
from .order_api import router as order_router
from .payment_api import router as payment_router
from .inventory_api import router as inventory_router
from .notification_api import router as notification_router
from .report_api import router as report_router
from .ai_api import router as ai_router
from .iot_api import router as iot_router
from .health_api import router as health_router

__all__ = [
    "auth_router",
    "dashboard_router",
    "customer_router",
    "order_router",
    "payment_router",
    "inventory_router",
    "notification_router",
    "report_router",
    "ai_router",
    "iot_router",
    "health_router",
]
