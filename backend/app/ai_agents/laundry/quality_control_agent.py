from app.ai_agents.shared.base_agent import BaseAgent
from app.ai_agents.shared.memory import Memory
from app.ai_agents.shared.llm_client import LLMClient
from app.ai_agents.shared.knowledge_base import KnowledgeBase


class QualityControlAgent(BaseAgent):
    """
    AI Agent untuk pemeriksaan kualitas hasil laundry.
    """

    def __init__(self):
        super().__init__(name="QualityControlAgent")
        self.memory = Memory()
        self.llm = LLMClient()
        self.kb = KnowledgeBase()

    async def process(self, qc_data: dict):
        """
        Analisis hasil quality control laundry.
        """

        order_id = qc_data.get("order_id")
        stain_status = qc_data.get("stain_status")
        ironing = qc_data.get("ironing")
        packaging = qc_data.get("packaging")

        prompt = f"""
        Analisis hasil Quality Control laundry berikut.

        Order ID : {order_id}
        Status Noda : {stain_status}
        Kualitas Setrika : {ironing}
        Status Packaging : {packaging}

        Berikan:
        - Status kelulusan QC
        - Temuan masalah
        - Tindakan perbaikan
        - Rekomendasi sebelum diserahkan ke pelanggan
        """

        response = await self.llm.generate(prompt)

        return {
            "status": "success",
            "agent": self.name,
            "analysis": response
        }
