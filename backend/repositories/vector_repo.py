import faiss
import numpy as np
import os
import pickle

FAISS_INDEX_PATH = "faiss_index.bin"
METADATA_PATH = "faiss_metadata.pkl"

class VectorRepository:
    def __init__(self, dimension: int = 384): # Default for all-MiniLM-L6-v2
        self.dimension = dimension
        if os.path.exists(FAISS_INDEX_PATH):
            self.index = faiss.read_index(FAISS_INDEX_PATH)
            with open(METADATA_PATH, "rb") as f:
                self.metadata_store = pickle.load(f)
            # Track the next vector ID to assign
            self.next_id = len(self.metadata_store) if self.metadata_store else 0
            # Ensure it's an IndexIDMap if we reloaded a generic one
            # If we saved it as IndexIDMap it loads correctly
        else:
            # We use an IndexIDMap to allow us to pass custom IDs
            base_index = faiss.IndexFlatL2(self.dimension)
            self.index = faiss.IndexIDMap(base_index)
            self.metadata_store = {}
            self.next_id = 0

    def add_embeddings(self, embeddings: np.ndarray, metadata_list: list) -> list:
        if len(embeddings) == 0:
            return []
            
        # Generate IDs
        ids = np.arange(self.next_id, self.next_id + len(embeddings), dtype=np.int64)
        
        # Add to FAISS index
        self.index.add_with_ids(embeddings, ids)
        
        # Add to metadata store
        added_ids = []
        for i, meta in enumerate(metadata_list):
            v_id = int(ids[i])
            self.metadata_store[v_id] = meta
            added_ids.append(v_id)
            
        self.next_id += len(embeddings)
        self._save()
        return added_ids

    def search(self, query_embedding: np.ndarray, k: int = 5):
        if self.index.ntotal == 0:
            return []
            
        distances, indices = self.index.search(query_embedding, k)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx != -1: # valid match
                meta = self.metadata_store.get(int(idx))
                if meta:
                    results.append({"distance": float(dist), "metadata": meta})
        return results

    def _save(self):
        faiss.write_index(self.index, FAISS_INDEX_PATH)
        with open(METADATA_PATH, "wb") as f:
            pickle.dump(self.metadata_store, f)

vector_repository = VectorRepository()
