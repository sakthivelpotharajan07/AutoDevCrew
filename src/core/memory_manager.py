import chromadb
from chromadb.config import Settings
from src.core.utils import load_config
from src.core.embedding_engine import EmbeddingEngine
import uuid

class MemoryManager:
    def __init__(self):
        config = load_config()
        self.client = chromadb.PersistentClient(path=config["memory"]["path"])
        self.collection_name = config["memory"]["collection"]
        self.embedding_engine = EmbeddingEngine()
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name
        )

    def add_memory(self, document: str, metadata: dict = None):
        """Adds a document to the memory."""
        embedding = self.embedding_engine.generate_embeddings([document])[0]
        self.collection.add(
            documents=[document],
            embeddings=[embedding],
            metadatas=[metadata] if metadata else [{}],
            ids=[str(uuid.uuid4())]
        )

    def search_memory(self, query: str, n_results=3):
        """Searches memory for similar documents."""
        embedding = self.embedding_engine.generate_embeddings([query])[0]
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results
        )
        return results
