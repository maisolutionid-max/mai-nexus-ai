from app.ai_agents.shared.base_agent import BaseAgent
from app.ai_agents.shared.memory import Memory
from app.ai_agents.shared.llm_client import LLMClientFactory
from app.ai_agents.shared.knowledge_base import KnowledgeBase


class InventoryAgent(BaseAgent):
    """AI Agent untuk pengelolaan inventaris laundry."""

    def __init__(self):
        super().__init__(name="InventoryAgent")
        self.memory = Memory()
        self.llm = LLMClientFactory.create(provider="mock")
        self.kb = KnowledgeBase()

    async def response(self, prompt: str) -> str:
        """Menghasilkan respons melalui LLM client."""
        return await self.llm.generate(prompt)

    async def process(self, inventory_data: dict) -> dict:
        """Menganalisis kebutuhan inventaris laundry."""

        item_name = inventory_data.get("item_name", "Tidak disebutkan")
        stock = inventory_data.get("stock", 0)
        minimum_stock = inventory_data.get("minimum_stock", 0)

        prompt = f"""
Analisis inventaris laundry berikut.

Nama barang: {item_name}
Stok saat ini: {stock}
Batas minimum stok: {minimum_stock}

Berikan status stok dan saran tindakan.
Jangan mengarang data di luar informasi yang tersedia.
"""

        analysis = await self.response(prompt)

        self.memory.add({
            "item_name": item_name,
            "stock": stock,
            "minimum_stock": minimum_stock,
            "analysis": analysis,
        })

        return {
            "status": "success",
            "agent": self.name,
            "analysis": analysis,
        }