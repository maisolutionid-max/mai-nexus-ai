
from app.ai_agents.shared.base_agent import BaseAgent
from app.ai_agents.shared.memory import Memory
from app.ai_agents.shared.llm_client import LLMClientFactory
from app.ai_agents.shared.knowledge_base import KnowledgeBase


class CustomerAgent(BaseAgent):
    """AI Agent untuk menangani pertanyaan dan kebutuhan pelanggan laundry."""

    def __init__(self):
        super().__init__(name="CustomerAgent")
        self.memory = Memory()
        self.llm = LLMClientFactory.create(provider="mock")
        self.kb = KnowledgeBase()

    async def response(self, prompt: str) -> str:
        """Menghasilkan respons melalui LLM client."""
        return await self.llm.generate(prompt)

    async def process(self, customer_data: dict) -> dict:
        """Memproses permintaan pelanggan."""

        customer_name = customer_data.get("name", "Pelanggan")
        question = customer_data.get(
            "question",
            customer_data.get("message", "")
        )

        if not question:
            return {
                "status": "error",
                "agent": self.name,
                "message": "Pertanyaan atau pesan pelanggan wajib diisi."
            }

        prompt = f"""
Kamu adalah asisten layanan pelanggan laundry.

Nama pelanggan: {customer_name}
Pertanyaan pelanggan: {question}

Jawab dengan sopan, jelas, singkat, dan membantu.
Jangan mengarang harga, status pesanan, atau waktu selesai
jika informasi tersebut tidak tersedia.
"""

        answer = await self.response(prompt)

        self.memory.add({
            "customer_name": customer_name,
            "question": question,
            "answer": answer,
        })

        return {
            "status": "success",
            "agent": self.name,
            "customer_name": customer_name,
            "answer": answer,
        }
