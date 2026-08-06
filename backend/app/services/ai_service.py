from app.ai_agents.shared.orchestrator import AgentOrchestrator

orchestrator = AgentOrchestrator()


def ask_ai(agent_name: str, payload: dict):
    return orchestrator.execute(agent_name, payload)
