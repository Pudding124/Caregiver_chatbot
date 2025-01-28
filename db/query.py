import chromadb
from sentence_transformers import SentenceTransformer
import json

chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection(name="rag_docs")

model = SentenceTransformer("intfloat/multilingual-e5-base")

query_text = "希望可以協助運動復健"
query_embedding = model.encode(["query: " + query_text])[0]

# 从 ChromaDB 查询最相似的 2 条数据
results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=2
)

# 输出查询结果（包含 ID）
print("查询结果：")
for doc_id, doc_text, score in zip(results["ids"][0], results["documents"][0], results["distances"][0]):
    print(f"ID: {doc_id}, 文档: {doc_text}, 相似度: {score:.4f}")