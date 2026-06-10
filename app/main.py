import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st

from ingestion.pdf_loader import extract_pdf_text
from ingestion.cleaner import clean_text
from chunking.chunker import chunk_text
from retrieval.retriever import retrieve_relevant_chunks


st.set_page_config(
    page_title="InsightFlow AI",
    page_icon="📄",
    layout="wide"
)

st.title("InsightFlow AI")
st.subheader(
    "AI Document Intelligence Platform for Business Decision Support"
)

uploaded_files = st.file_uploader(
    "Upload PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)

all_chunk_records = []

if uploaded_files:

    for file in uploaded_files:

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

        st.success(f"{file.name} processed")

        st.write(f"Characters: {len(cleaned_text)}")
        st.write(f"Chunks: {len(chunks)}")

        for i, chunk in enumerate(chunks[:3]):

            with st.expander(f"Chunk {i+1}"):

                st.write(chunk)


st.divider()

question = st.text_input(
    "Ask a question about your documents"
)

if st.button("Search Relevant Chunks"):

    if question and all_chunk_records:

        results = retrieve_relevant_chunks(
            question,
            all_chunk_records
        )

        st.write("## Top Relevant Chunks")

        for result in results:

            with st.expander(
                f"{result['document_name']} | Chunk {result['chunk_id']} | Score {result['score']}"
            ):

                st.write(result["text"])

    else:

        st.warning(
            "Upload document and enter question"
        )