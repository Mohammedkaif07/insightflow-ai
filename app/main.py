import sys
from pathlib import Path

# Add project root folder to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
from ingestion.pdf_loader import extract_pdf_text


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

if uploaded_files:
    for file in uploaded_files:
        st.success(f"Uploaded: {file.name}")

        extracted_text = extract_pdf_text(file)

        st.text_area(
            label=f"Extracted text from {file.name}",
            value=extracted_text[:3000],
            height=300
        )

st.divider()

question = st.text_input("Ask a question about your documents")

if st.button("Generate Answer"):
    if question:
        st.info("RAG pipeline will be connected in the next phase.")
    else:
        st.warning("Please enter a question first.")