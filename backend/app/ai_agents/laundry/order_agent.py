from app.ai_agents.shared.base_agent import BaseAgent
from app.ai_agents.shared.memory import Memory
from app.ai_agents.shared.llm_client import LLMClient
from app.ai_agents.shared.knowledge_base import KnowledgeBase


class OrderAgent(BaseAgent):
    """
    AI Agent untuk menangani order laundry.
    """

    def __init__(self):
        super().__init__(name="OrderAgent")
        self.memory = Memory()
        self.llm = LLMClient()
        self.kb = KnowledgeBase()

    async def process(self, order_data: dict):
        """
        Memproses order laundry.
        """
        customer = order_data.get("customer")
        service = order_data.get("service")
        weight = order_data.get("weight")

        prompt = f"""
        Analisis order laundry berikut.

        Customer : {customer}
        Service  : {service}
        Berat    : {weight} Kg

        Berikan:
        - Estimasi selesai
        - Prioritas pengerjaan
        - Catatan operasional
        """

        response = await self.llm.generate(prompt)

        return {
            "status": "success",
            "agent": self.name,
            "analysis": response
        }
