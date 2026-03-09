from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingService:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # This will download the model on first initialization
        self.model = SentenceTransformer(model_name)
        
    def generate_embedding(self, text: str) -> np.ndarray:
        embedding = self.model.encode(text)
        # Reshape for FAISS if single embedding
        return np.array([embedding], dtype=np.float32)

    def generate_embeddings_batch(self, texts: list[str]) -> np.ndarray:
        embeddings = self.model.encode(texts)
        return np.array(embeddings, dtype=np.float32)

embedding_service = EmbeddingService()
