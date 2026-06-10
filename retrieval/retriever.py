from sklearn.metrics.pairwise import cosine_similarity
from embedding.embedder import create_embeddings


def retrieve_relevant_chunks(question, chunk_records, top_k=3):
    if not question or not chunk_records:
        return []

    chunk_texts = [record["text"] for record in chunk_records]

    chunk_embeddings = create_embeddings(chunk_texts)
    question_embedding = create_embeddings([question])

    similarities = cosine_similarity(question_embedding, chunk_embeddings)[0]

    ranked_results = sorted(
        enumerate(similarities),
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    for index, score in ranked_results[:top_k]:
        record = chunk_records[index]

        results.append(
            {
                "document_name": record["document_name"],
                "chunk_id": record["chunk_id"],
                "score": round(float(score), 3),
                "text": record["text"],
            }
        )

    return results