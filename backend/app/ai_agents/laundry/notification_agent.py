from app.ai_agents.shared.base_agent import BaseAgent
from app.ai_agents.shared.memory import Memory
from app.ai_agents.shared.llm_client import LLMClient
from app.ai_agents.shared.knowledge_base import KnowledgeBase


class NotificationAgent(BaseAgent):
    """
    AI Agent untuk mengelola notifikasi pelanggan
    dan operasional laundry.
    """

    def __init__(self):
        super().__init__(name="NotificationAgent")
        self.memory = Memory()
        self.llm = LLMClient()
        self.kb = KnowledgeBase()

    async def process(self, notification_data: dict):
        """
        Membuat notifikasi berdasarkan event.
        """

        event = notification_data.get("event")
        customer_name = notification_data.get("customer_name")
        phone = notification_data.get("phone")
        email = notification_data.get("email")
        order_number = notification_data.get("order_number")
        status = notification_data.get("status")
        estimated_finish = notification_data.get("estimated_finish")

        prompt = f"""
        Buatkan notifikasi profesional.

        Event : {event}
        Nama : {customer_name}
        Order : {order_number}
        Status : {status}
        Estimasi : {estimated_finish}

        Hasilkan:

        1. WhatsApp Message
        2. Email Message
        3. Push Notification
        """

        response = await self.llm.generate(prompt)

        return {
            "status": "success",
            "agent": self.name,
            "event": event,
            "recipient": {
                "phone": phone,
                "email": email
            },
            "message": response
        }
