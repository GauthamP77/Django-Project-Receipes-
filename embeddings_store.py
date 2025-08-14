from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

class FAISSSearch:
    def __init__(self):
        self.index = None
        self.chunks = []

    def build(self, chunks):
        """Build the FAISS index from a list of chunks."""
        self.chunks = chunks
        if not chunks:
            # Avoid building index with no data
            return
        texts = [c["text"] for c in chunks]
        embeddings = embedding_model.encode(texts, convert_to_numpy=True)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def search(self, query, top_k=5):
        """Search for top_k most similar chunks to the query."""
        if not self.chunks or self.index is None:
            # No index/chunks to search
            return []

        query_emb = embedding_model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_emb, top_k)

        results = []
        for idx in indices[0]:
            # ✅ Check index validity & filter out invalid (-1) placeholders
            if idx != -1 and 0 <= idx < len(self.chunks):
                results.append(self.chunks[idx])

        return results
