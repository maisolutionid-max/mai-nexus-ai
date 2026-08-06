class KnowledgeBase:

    def __init__(self):
        self.documents = {}

    def add_document(self, key, content):
        self.documents[key] = content

    def get_document(self, key):
        return self.documents.get(key)

    def search(self, keyword):
        result = []
        for key, value in self.documents.items():
            if keyword.lower() in str(value).lower():
                result.append({key: value})
        return result
