from ai_agents.shared.base_agent import BaseAgent
from ai_agents.laundry.pricing import calculate_price
from ai_agents.laundry.recommendation import generate_recommendation


class LaundryAgent(BaseAgent):

    def __init__(self):
        super().__init__("Laundry Agent")

    def process(self, data: dict):

        result = {
            "price": calculate_price(
                data.get("service_type"),
                data.get("weight")
            ),
            "recommendation": generate_recommendation(data)
        }

        return result

    def response(self, result):

        return {
            "agent": self.name,
            "result": result
        }

    def chat(self, question: str):

        return {
            "agent": self.name,
            "message": question,
            "answer": "AI response placeholder"
      }
