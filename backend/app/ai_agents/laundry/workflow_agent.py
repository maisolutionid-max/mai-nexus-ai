from app.ai_agents.shared.base_agent import BaseAgent
from app.ai_agents.shared.agent_registry import AgentRegistry


class WorkflowAgent(BaseAgent):
    """
    AI Workflow Agent

    Mengorkestrasi seluruh AI Agent pada proses bisnis laundry.
    """

    def __init__(self):
        super().__init__(name="WorkflowAgent")
        self.registry = AgentRegistry()

    async def process(self, workflow_data: dict):

        workflow = []

        # Order
        order_agent = self.registry.get("order")
        if order_agent:
            workflow.append(
                await order_agent.process(workflow_data)
            )

        # Customer
        customer_agent = self.registry.get("customer")
        if customer_agent:
            workflow.append(
                await customer_agent.process(workflow_data)
            )

        # Inventory
        inventory_agent = self.registry.get("inventory")
        if inventory_agent:
            workflow.append(
                await inventory_agent.process(workflow_data)
            )

        # Chemical
        chemical_agent = self.registry.get("chemical")
        if chemical_agent:
            workflow.append(
                await chemical_agent.process(workflow_data)
            )

        # Quality Control
        qc_agent = self.registry.get("quality_control")
        if qc_agent:
            workflow.append(
                await qc_agent.process(workflow_data)
            )

        # Predictive Maintenance
        predictive_agent = self.registry.get("predictive_maintenance")
        if predictive_agent:
            workflow.append(
                await predictive_agent.process(workflow_data)
            )

        # Analytics
        analytics_agent = self.registry.get("analytics")
        if analytics_agent:
            workflow.append(
                await analytics_agent.process(workflow_data)
            )

        # Notification
        notification_agent = self.registry.get("notification")
        if notification_agent:
            workflow.append(
                await notification_agent.process(workflow_data)
            )

        return {
            "status": "success",
            "agent": self.name,
            "workflow": workflow
              }
