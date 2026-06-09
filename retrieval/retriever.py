def retrieve_from_chroma(question):
    return [
        {
            "document_name": "Test",
            "chunk_id": 1,
            "score": 0.99,
            "text": f"Question received: {question}"
        }
    ]