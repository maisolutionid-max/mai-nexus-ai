"""
MAI Nexus AI
Service Container

Central Dependency Injection Container
Author : MAI Solution Hub
"""

from functools import lru_cache

from app.services.customer_service import CustomerService
from app.services.order_service import OrderService
from app.services.payment_service import PaymentService
from app.services.dashboard_service import DashboardService
from app.services.ai_service import AIService


class ServiceContainer:
    """
    Central service registry.

    Semua service backend diinisialisasi satu kali
    dan digunakan oleh seluruh API Router.

    Tujuan:
    - Menghindari duplicate object
    - Dependency Injection
    - Single Source of Truth
    """

    def __init__(self):

        # Business Services
        self.customer_service = CustomerService()
        self.order_service = OrderService()
        self.payment_service = PaymentService()
        self.dashboard_service = DashboardService()

        # AI Layer
        self.ai_service = AIService()


@lru_cache
def get_container() -> ServiceContainer:
    """
    Singleton Service Container.
    """
    return ServiceContainer()
