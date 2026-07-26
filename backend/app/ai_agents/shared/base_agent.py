from abc import ABC, abstractmethod


class BaseAgent(ABC):

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def process(self, data: dict):
        pass

    @abstractmethod
    def response(self, result):
        pass
