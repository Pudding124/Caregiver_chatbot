import chromadb
from sentence_transformers import SentenceTransformer
import json

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="rag_docs")

model = SentenceTransformer("intfloat/multilingual-e5-base")

with open('../data_pipeline/pre_embedding_data.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

for content in data:
    embedding = model.encode("passage: " + content['doc']).tolist()
    
    collection.add(
        ids=[content['id']],
        documents=[content['doc']],
        embeddings=[embedding]
    )

print(f"已存入 {collection.count()} 条数据")
