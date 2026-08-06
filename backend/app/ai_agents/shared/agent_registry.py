from app.ai_agents.laundry.order_agent import OrderAgent
from app.ai_agents.laundry.customer_agent import CustomerAgent
from app.ai_agents.laundry.inventory_agent import InventoryAgent
from app.ai_agents.laundry.quality_control_agent import QualityControlAgent
from app.ai_agents.laundry.chemical_agent import ChemicalAgent
from app.ai_agents.laundry.predictive_maintenance_agent import PredictiveMaintenanceAgent
from app.ai_agents.laundry.analytics_agent import AnalyticsAgent
from app.ai_agents.laundry.notification_agent import NotificationAgent


class AgentRegistry:

    def __init__(self):
        self.agents = {
            "order": OrderAgent(),
            "customer": CustomerAgent(),
            "inventory": InventoryAgent(),
            "quality_control": QualityControlAgent(),
            "chemical": ChemicalAgent(),
            "predictive_maintenance": PredictiveMaintenanceAgent(),
            "analytics": AnalyticsAgent(),
            "notification": NotificationAgent(),
        }

    def get(self, name):
        return self.agents.get(name)

    def all(self):
        return self.agents
