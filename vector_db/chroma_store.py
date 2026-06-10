import chromadb

client = chromadb.Client()

collection = client.get_or_create_collection(
    name="insightflow_documents"
)


def store_chunks(chunk_records, embeddings):
    ids = []
    documents = []
    metadatas = []

    for record in chunk_records:
        doc_name = record["document_name"].replace(" ", "_")
        chunk_id = str(record["chunk_id"])

        ids.append(f"{doc_name}_chunk_{chunk_id}")
        documents.append(record["text"])

        metadatas.append(
            {
                "document_name": record["document_name"],
                "chunk_id": chunk_id
            }
        )

    collection.upsert(
        ids=ids,
        documents=documents,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )


def search_chunks(question_embedding, top_k=3):
    results = collection.query(
        query_embeddings=question_embedding.tolist(),
        n_results=top_k
    )

    return results