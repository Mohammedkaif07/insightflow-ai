def chunk_text(text: str, chunk_size: int = 200, overlap: int = 50):
    if not text:
        return []

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = words[start:end]
        chunks.append(" ".join(chunk))

        start = end - overlap

        if start >= len(words):
            break

    return chunks