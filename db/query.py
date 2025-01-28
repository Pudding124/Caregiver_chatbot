import chromadb
from sentence_transformers import SentenceTransformer
import json

class Chroma():

    def __init__(self):
        self.chroma_client = chromadb.PersistentClient(path="E://taiwan_care/db/chroma_db")
        self.collection = self.chroma_client.get_or_create_collection(name="rag_docs")
        self.model = SentenceTransformer("intfloat/multilingual-e5-base")

    def get_top3_result(self, feature):
        feature_list = ", ".join(feature)
        query_embedding = self.model.encode(["query: " + feature_list])[0]
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=3
        )
        all_doc_id = []
        all_doc_text = []
        for doc_id, doc_text, score in zip(results["ids"][0], results["documents"][0], results["distances"][0]):
            all_doc_id.append(doc_id)
            all_doc_text.append(doc_text[:30] + "...")
            # print(f"ID: {doc_id}, 文档: {doc_text}, 相似度: {score:.4f}")
        
        return all_doc_id, all_doc_text
