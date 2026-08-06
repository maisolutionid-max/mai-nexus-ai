from app.ai_agents.shared.base_agent import BaseAgent
from app.ai_agents.shared.memory import Memory
from app.ai_agents.shared.llm_client import LLMClient
from app.ai_agents.shared.knowledge_base import KnowledgeBase


class PredictiveMaintenanceAgent(BaseAgent):
    """
    AI Agent untuk prediksi perawatan mesin laundry berdasarkan
    data sensor dan histori operasional.
    """

    def __init__(self):
        super().__init__(name="PredictiveMaintenanceAgent")
        self.memory = Memory()
        self.llm = LLMClient()
        self.kb = KnowledgeBase()

    async def process(self, machine_data: dict):
        """
        Analisis kondisi mesin laundry.
        """

        machine_id = machine_data.get("machine_id")
        runtime_hours = machine_data.get("runtime_hours")
        temperature = machine_data.get("temperature")
        vibration = machine_data.get("vibration")
        energy = machine_data.get("energy")
        last_service = machine_data.get("last_service")

        prompt = f"""
        Analisis kondisi mesin laundry berikut.

        Machine ID : {machine_id}
        Jam Operasi : {runtime_hours}
        Suhu Mesin : {temperature} °C
        Getaran : {vibration}
        Konsumsi Energi : {energy} kWh
        Service Terakhir : {last_service}

        Berikan analisis:

        - Health Score mesin (0–100)
        - Risiko kerusakan
        - Komponen yang perlu diperiksa
        - Estimasi waktu maintenance berikutnya
        - Prioritas maintenance
        - Rekomendasi tindakan
        """

        response = await self.llm.generate(prompt)

        return {
            "status": "success",
            "agent": self.name,
            "machine_id": machine_id,
            "analysis": response
        }
