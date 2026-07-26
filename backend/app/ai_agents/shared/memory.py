class AgentMemory:

    def __init__(self):
        self.memory = []

    def add(self, data):
        self.memory.append(data)

    def history(self):
        return self.memory

    def clear(self):
        self.memory.clear()
