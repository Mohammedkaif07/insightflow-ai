import streamlit as st

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
    st.success(f"{len(uploaded_files)} document(s) uploaded successfully.")

    for file in uploaded_files:
        st.write(f"Uploaded: {file.name}")

st.divider()

question = st.text_input("Ask a question about your documents")

if st.button("Generate Answer"):
    if question:
        st.info("RAG pipeline will be connected in the next phase.")
    else:
        st.warning("Please enter a question first.")