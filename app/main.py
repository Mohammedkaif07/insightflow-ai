import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st

from ingestion.pdf_loader import extract_pdf_text
from ingestion.cleaner import clean_text
from chunking.chunker import chunk_text
from embedding.embedder import create_embeddings
from vector_db.chroma_store import store_chunks
from retrieval.chroma_retriever import search_chroma


st.set_page_config(
    page_title="InsightFlow AI",
    page_icon="📄",
    layout="wide"
)

st.title("InsightFlow AI")
st.subheader("AI Document Intelligence Platform for Business Decision Support")

st.write(
    "Upload business documents, ask questions, get cited insights, and generate decisions."
)

st.divider()

uploaded_files = st.file_uploader(
    "Upload PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)

all_chunk_records = []

if uploaded_files:
    st.success(f"{len(uploaded_files)} document(s) uploaded successfully.")

    for file in uploaded_files:
        with st.expander(f"Preview: {file.name}", expanded=True):
            raw_text = extract_pdf_text(file)
            cleaned_text = clean_text(raw_text)
            chunks = chunk_text(cleaned_text)

            for index, chunk in enumerate(chunks):
                all_chunk_records.append(
                    {
                        "document_name": file.name,
                        "chunk_id": index + 1,
                        "text": chunk
                    }
                )

            col1, col2 = st.columns(2)

            with col1:
                st.write("### Raw Extracted Text")
                st.text_area(
                    "Before cleaning",
                    raw_text[:3000],
                    height=350,
                    key=f"raw_{file.name}"
                )

            with col2:
                st.write("### Cleaned Text")
                st.text_area(
                    "After cleaning",
                    cleaned_text[:3000],
                    height=350,
                    key=f"cleaned_{file.name}"
                )

            st.write("### Processing Stats")
            st.write(f"Raw characters: {len(raw_text)}")
            st.write(f"Cleaned characters: {len(cleaned_text)}")
            st.write(f"Raw words: {len(raw_text.split())}")
            st.write(f"Cleaned words: {len(cleaned_text.split())}")
            st.write(f"Total chunks created: {len(chunks)}")

            if chunks:
                st.write("### Chunk Preview")
                for i, chunk in enumerate(chunks[:3]):
                    with st.expander(f"Chunk {i + 1}"):
                        st.write(chunk)

    if all_chunk_records:
        with st.spinner("Storing document chunks in ChromaDB..."):
            chunk_texts = [record["text"] for record in all_chunk_records]
            chunk_embeddings = create_embeddings(chunk_texts)
            store_chunks(all_chunk_records, chunk_embeddings)

        st.success("Document chunks stored in ChromaDB.")

st.divider()

question = st.text_input("Ask a question about your documents")

if st.button("Search Relevant Chunks"):
    if question:
        with st.spinner("Searching ChromaDB..."):
            results = search_chroma(question)

        st.write("### Top Relevant Chunks")

        if results:
            for result in results:
                with st.expander(
                    f"{result['document_name']} | Chunk {result['chunk_id']} | Score: {result['score']}"
                ):
                    st.write(result["text"])
        else:
            st.warning("No relevant chunks found.")
    else:
        st.warning("Please enter a question first.")