from app.ai_agents.shared.base_agent import BaseAgent
from app.ai_agents.shared.memory import Memory
from app.ai_agents.shared.llm_client import LLMClient
from app.ai_agents.shared.knowledge_base import KnowledgeBase


class CustomerAgent(BaseAgent):
    """
    AI Agent untuk mengelola hubungan pelanggan.
    """

    def __init__(self):
        super().__init__(name="CustomerAgent")
        self.memory = Memory()
        self.llm = LLMClient()
        self.kb = KnowledgeBase()

    async def process(self, customer_data: dict):
        """
        Analisis data pelanggan.
        """

        name = customer_data.get("name")
        total_orders = customer_data.get("total_orders", 0)
        last_visit = customer_data.get("last_visit")

        prompt = f"""
        Analisis pelanggan laundry berikut.

        Nama : {name}
        Total Order : {total_orders}
        Kunjungan Terakhir : {last_visit}

        Berikan:
        - Tingkat loyalitas pelanggan
        - Risiko pelanggan tidak kembali
        - Rekomendasi promosi
        - Rekomendasi layanan berikutnya
        """

        response = await self.llm.generate(prompt)

        return {
            "status": "success",
            "agent": self.name,
            "analysis": response
        }
