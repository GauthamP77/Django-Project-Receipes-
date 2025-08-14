import streamlit as st
import os
from pdf_processing import extract_text_from_pdf, chunk_text
from embeddings_store import FAISSSearch
from llm_answer import get_llm_answer
from config import TOP_N_RESULTS

st.set_page_config(page_title="StudyMate - AI Academic Assistant", layout="wide")

st.title("📚 StudyMate")
st.write("Upload your academic PDFs and ask context-based questions. Answers are based strictly on your files.")

# ✅ Initialise the variable before using it anywhere
all_chunks = []

uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)
query = st.text_input("Ask a question:")

if uploaded_files:
    os.makedirs("temp_storage", exist_ok=True)
    for file in uploaded_files:
        file_path = os.path.join("temp_storage", file.name)
        with open(file_path, "wb") as f:
            f.write(file.read())
        pages = extract_text_from_pdf(file_path)
        chunks = chunk_text(pages)
        all_chunks.extend(chunks)

# ✅ Check before building FAISS
if query:
    if not all_chunks:
        st.error("No text chunks found. Please upload readable PDF files first.")
        st.stop()

    vector_store = FAISSSearch()
    vector_store.build(all_chunks)
    relevant_chunks = vector_store.search(query, top_k=TOP_N_RESULTS)
    answer = get_llm_answer(query, relevant_chunks)

    st.markdown("### 📝 Answer")
    st.write(answer)

    st.markdown("### 📄 Sources")
    for c in relevant_chunks:
        st.write(f"Page {c['page']}: {c['text'][:200]}...")
