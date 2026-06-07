from sentence_transformers import SentenceTransformer


_model = None


def load_embedding_model():
    global _model

    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    return _model


def create_embeddings(texts):
    clean_texts = []

    for item in texts:
        if isinstance(item, dict):
            clean_texts.append(str(item.get("text", "")))
        else:
            clean_texts.append(str(item))

    model = load_embedding_model()
    return model.encode(clean_texts, convert_to_tensor=False)