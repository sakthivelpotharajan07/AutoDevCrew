from sentence_transformers import SentenceTransformer
from src.core.utils import load_config

class EmbeddingEngine:
    def __init__(self):
        config = load_config()
        model_name = config.get("embeddings", {}).get("model", "all-MiniLM-L6-v2")
        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, text_list):
        return self.model.encode(text_list).tolist()
