from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseLLMClient(ABC):
    """
    Base interface untuk semua Large Language Model.
    """

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        pass


class MockLLMClient(BaseLLMClient):
    """
    Mock client untuk development sebelum API LLM dihubungkan.
    """

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:

        return f"[MOCK RESPONSE]\\n{prompt}"


class LLMClientFactory:

    @staticmethod
    def create(provider: str = "mock") -> BaseLLMClient:

        provider = provider.lower()

        if provider == "mock":
            return MockLLMClient()

        raise ValueError(f"Unsupported LLM Provider: {provider}")
