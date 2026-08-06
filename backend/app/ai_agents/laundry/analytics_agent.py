from app.ai_agents.shared.base_agent import BaseAgent
from app.ai_agents.shared.memory import Memory
from app.ai_agents.shared.llm_client import LLMClient
from app.ai_agents.shared.knowledge_base import KnowledgeBase


class AnalyticsAgent(BaseAgent):
    """
    AI Agent untuk analisis bisnis laundry.
    Menghasilkan insight operasional dan rekomendasi strategis.
    """

    def __init__(self):
        super().__init__(name="AnalyticsAgent")
        self.memory = Memory()
        self.llm = LLMClient()
        self.kb = KnowledgeBase()

    async def process(self, analytics_data: dict):
        """
        Analisis performa bisnis laundry.
        """

        total_orders = analytics_data.get("total_orders", 0)
        total_revenue = analytics_data.get("total_revenue", 0)
        active_customers = analytics_data.get("active_customers", 0)
        average_order = analytics_data.get("average_order", 0)
        machine_utilization = analytics_data.get("machine_utilization", 0)
        low_stock_items = analytics_data.get("low_stock_items", [])

        prompt = f"""
        Analisis performa bisnis laundry berikut.

        Total Order : {total_orders}
        Total Pendapatan : Rp {total_revenue}
        Pelanggan Aktif : {active_customers}
        Rata-rata Order : Rp {average_order}
        Utilisasi Mesin : {machine_utilization}%
        Stok Menipis : {low_stock_items}

        Berikan analisis:

        1. Ringkasan performa bisnis
        2. KPI utama
        3. Risiko operasional
        4. Peluang peningkatan pendapatan
        5. Rekomendasi efisiensi biaya
        6. Rekomendasi tindakan prioritas
        """

        response = await self.llm.generate(prompt)

        return {
            "status": "success",
            "agent": self.name,
            "analysis": response,
            "summary": {
                "orders": total_orders,
                "revenue": total_revenue,
                "customers": active_customers
            }
        }
