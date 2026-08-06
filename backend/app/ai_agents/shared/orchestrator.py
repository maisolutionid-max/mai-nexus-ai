from .agent_registry import AgentRegistry


class AgentOrchestrator:

    def __init__(self):
        self.registry = AgentRegistry()

    def execute(self, agent_name: str, payload: dict):
        agent = self.registry.get(agent_name)

        if not agent:
            return {
                "success": False,
                "message": f"Agent '{agent_name}' tidak ditemukan."
            }

        return agent.run(payload)
