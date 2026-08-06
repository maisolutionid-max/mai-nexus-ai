from app.ai_agents.shared.base_agent import BaseAgent
from app.ai_agents.shared.memory import Memory
from app.ai_agents.shared.llm_client import LLMClient
from app.ai_agents.shared.knowledge_base import KnowledgeBase


class InventoryAgent(BaseAgent):
    """
    AI Agent untuk mengelola persediaan laundry.
    """

    def __init__(self):
        super().__init__(name="InventoryAgent")
        self.memory = Memory()
        self.llm = LLMClient()
        self.kb = KnowledgeBase()

    async def process(self, inventory_data: dict):
        """
        Analisis kondisi persediaan.
        """

        item = inventory_data.get("item")
        stock = inventory_data.get("stock")
        minimum_stock = inventory_data.get("minimum_stock")

        prompt = f"""
        Analisis persediaan laundry berikut.

        Item : {item}
        Stok Saat Ini : {stock}
        Minimum Stok : {minimum_stock}

        Berikan:
        - Status stok
        - Risiko kehabisan stok
        - Rekomendasi pembelian
        - Prioritas pengadaan
        """

        response = await self.llm.generate(prompt)

        return {
            "status": "success",
            "agent": self.name,
            "analysis": response
        }
