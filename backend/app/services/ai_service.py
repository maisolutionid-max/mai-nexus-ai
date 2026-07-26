from ai_agents.laundry.laundry_agent import LaundryAgent


agent = LaundryAgent()


def ask_ai(question: str):

    return agent.chat(question)
