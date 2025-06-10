import numpy as np
import faiss
import pickle
import os
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
from config import settings
import pinecone
from models import LegalFinding

class VectorStore:
    def __init__(self, use_pinecone: bool = False):
        self.use_pinecone = use_pinecone
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = settings.vector_dimension
        
        if use_pinecone and settings.pinecone_api_key:
            self._init_pinecone()
        else:
            self._init_faiss()
    
    def _init_pinecone(self):
        pinecone.init(
            api_key=settings.pinecone_api_key,
            environment=settings.pinecone_environment
        )
        
        if settings.index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=settings.index_name,
                dimension=self.dimension,
                metric='cosine'
            )
        
        self.index = pinecone.Index(settings.index_name)
    
    def _init_faiss(self):
        self.index = faiss.IndexFlatIP(self.dimension)
        self.documents = []
        self.metadata = []
        self._load_local_index()
    
    def _load_local_index(self):
        if os.path.exists("faiss_index.bin") and os.path.exists("metadata.pkl"):
            self.index = faiss.read_index("faiss_index.bin")
            with open("metadata.pkl", "rb") as f:
                self.metadata = pickle.load(f)
    
    def _save_local_index(self):
        faiss.write_index(self.index, "faiss_index.bin")
        with open("metadata.pkl", "wb") as f:
            pickle.dump(self.metadata, f)
    
    def add_documents(self, documents: List[str], metadata: List[Dict[str, Any]]):
        embeddings = self.embedder.encode(documents)
        
        if self.use_pinecone:
            vectors = [
                (str(i), embedding.tolist(), meta) 
                for i, (embedding, meta) in enumerate(zip(embeddings, metadata))
            ]
            self.index.upsert(vectors)
        else:
            self.index.add(embeddings)
            self.metadata.extend(metadata)
            self._save_local_index()
    
    def search(self, query: str, k: int = 5) -> List[Dict[str, Any]]:
        query_embedding = self.embedder.encode([query])
        
        if self.use_pinecone:
            results = self.index.query(
                vector=query_embedding[0].tolist(),
                top_k=k,
                include_metadata=True
            )
            return [
                {
                    "content": match.metadata.get("content", ""),
                    "score": match.score,
                    "metadata": match.metadata
                }
                for match in results.matches
            ]
        else:
            scores, indices = self.index.search(query_embedding, k)
            return [
                {
                    "content": self.metadata[idx].get("content", ""),
                    "score": float(scores[0][i]),
                    "metadata": self.metadata[idx]
                }
                for i, idx in enumerate(indices[0]) if idx < len(self.metadata)
            ]

vector_store = VectorStore() 