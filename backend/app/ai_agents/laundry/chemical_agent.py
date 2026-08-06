from app.ai_agents.shared.base_agent import BaseAgent
from app.ai_agents.shared.memory import Memory
from app.ai_agents.shared.llm_client import LLMClient
from app.ai_agents.shared.knowledge_base import KnowledgeBase


class ChemicalAgent(BaseAgent):
    """
    AI Agent untuk optimasi penggunaan bahan kimia laundry.
    """

    def __init__(self):
        super().__init__(name="ChemicalAgent")
        self.memory = Memory()
        self.llm = LLMClient()
        self.kb = KnowledgeBase()

    async def process(self, chemical_data: dict):
        """
        Analisis penggunaan bahan kimia laundry.
        """

        fabric_type = chemical_data.get("fabric_type")
        stain_level = chemical_data.get("stain_level")
        weight = chemical_data.get("weight")
        machine_type = chemical_data.get("machine_type")

        prompt = f"""
        Analisis penggunaan bahan kimia laundry berikut.

        Jenis Kain : {fabric_type}
        Tingkat Kekotoran : {stain_level}
        Berat Cucian : {weight} Kg
        Mesin : {machine_type}

        Berikan rekomendasi:

        - Jenis deterjen
        - Dosis deterjen
        - Dosis softener
        - Dosis bleach (jika diperlukan)
        - Suhu air
        - Lama pencucian
        - Tingkat keamanan terhadap kain
        - Estimasi biaya bahan kimia
        """

        response = await self.llm.generate(prompt)

        return {
            "status": "success",
            "agent": self.name,
            "analysis": response
        }
