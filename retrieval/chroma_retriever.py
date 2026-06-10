from embedding.embedder import create_embeddings
from vector_db.chroma_store import search_chunks


def search_chroma(question, top_k=3):
    if not question:
        return []

    question_embedding = create_embeddings([question])

    results = search_chunks(
        question_embedding,
        top_k=top_k
    )

    output = []

    if not results or not results.get("documents"):
        return output

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i in range(len(documents)):
        output.append(
            {
                "document_name": metadatas[i].get("document_name", "Unknown"),
                "chunk_id": metadatas[i].get("chunk_id", "Unknown"),
                "score": round(float(distances[i]), 3),
                "text": documents[i],
            }
        )

    return output