import json

class EmbeddingInfo:
    def __init__(self, id, doc):
        self.id = id
        self.doc = doc
    
    def to_dict(self):
        return {
            "id": self.id,
            "doc": self.doc
        }

with open('tide_up_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

pre_embedding_data = []

for person in data:
    id = person['id']
    doc = f"{person['description']}, 能夠提供的服務有{person['service_rule']}"

    embedding = EmbeddingInfo(id, doc)
    pre_embedding_data.append(embedding.to_dict())

# Write data to a JSON file
with open('pre_embedding_data.json', 'w', encoding='utf-8') as file:
    json.dump(pre_embedding_data, file, ensure_ascii=False, indent=4)