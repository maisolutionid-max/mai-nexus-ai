from typing import Dict

from .base_agent import BaseAgent


class AgentRegistry:

    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}

    def register(self, name: str, agent: BaseAgent):
        self._agents[name] = agent

    def get(self, name: str):
        return self._agents.get(name)

    def all(self):
        return self._agents

    def exists(self, name: str):
        return name in self._agents
