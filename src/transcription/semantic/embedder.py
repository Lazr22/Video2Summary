from sentence_transformers import SentenceTransformer

# Global model variable (loaded once)
_model = None


def load_embedder(model_name: str = "all-MiniLM-L6-v2"):
    global _model

    if _model is None:
        _model = SentenceTransformer(model_name)

    return _model


def embed_sentences(sentences: list[str]) -> list[list[float]]:
    model = load_embedder()

    embeddings = model.encode(sentences, normalize_embeddings=True)

    return embeddings.tolist()