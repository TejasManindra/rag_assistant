import sys
import os
import time

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import streamlit as st

from backend.pdf_loader import extract_text
from backend.chunker import create_chunks
from backend.embeddings import get_embeddings
from backend.vector_store import (
    store_chunks,
    clear_collection
)
from backend.retriever import retrieve
from backend.rag_chain import generate_answer

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Document Assistant")
st.markdown(
    "Upload a PDF, process it, and ask questions about its contents."
)

# =========================
# SESSION STATE
# =========================

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

# =========================
# PDF UPLOAD
# =========================

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file is not None:

    os.makedirs("uploads", exist_ok=True)

    pdf_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(
        f"✅ Uploaded: {uploaded_file.name}"
    )

    if st.button("🚀 Process PDF"):

        with st.spinner("Processing PDF..."):

            start = time.time()

            # Extract text
            text = extract_text(pdf_path)

            st.write("Text Length:", len(text))
            print("Text Length:", len(text))

            # Create chunks
            chunks = create_chunks(text)

            st.write("Chunks:", len(chunks))
            print("Chunks:", len(chunks))

            if len(chunks) == 0:
                st.error(
                    "❌ No text could be extracted from this PDF."
                )
                st.stop()

            # Create embeddings
            embeddings = get_embeddings(chunks)

            st.write("Embeddings:", len(embeddings))
            print("Embeddings:", len(embeddings))

            if len(embeddings) == 0:
                st.error(
                    "❌ Embedding generation failed."
                )
                st.stop()

            # Clear old document
            clear_collection()

            # Store in ChromaDB
            store_chunks(
                chunks,
                embeddings
            )

            processing_time = (
                time.time() - start
            )

        st.session_state.pdf_processed = True

        st.success(
            "✅ PDF processed successfully!"
        )

        st.info(
            f"Chunks Created: {len(chunks)} | "
            f"Processing Time: {processing_time:.2f}s"
        )

# =========================
# QUESTION ANSWERING
# =========================

st.divider()

question = st.text_input(
    "Ask a question about the document"
)

if question:

    if not st.session_state.pdf_processed:

        st.warning(
            "⚠️ Please upload and process a PDF first."
        )

    else:

        with st.spinner(
            "Searching document and generating answer..."
        ):

            # Retrieval
            start = time.time()

            results = retrieve(question)

            retrieval_time = (
                time.time() - start
            )

            docs = list(
                dict.fromkeys(
                    results["documents"][0]
                )
            )

            context = "\n".join(
                docs[:4]
            )

            # LLM
            start = time.time()

            answer = generate_answer(
                question,
                context
            )

            llm_time = (
                time.time() - start
            )

        # Answer
        st.subheader("📌 Answer")
        st.write(answer)

        # Sources
        with st.expander(
            "📚 Retrieved Sources"
        ):

            for i, doc in enumerate(
                docs[:4],
                start=1
            ):

                st.markdown(
                    f"### Source {i}"
                )

                st.write(doc)

                st.divider()

        # Metrics
        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Retrieval Time",
                f"{retrieval_time:.2f}s"
            )

        with col2:
            st.metric(
                "LLM Time",
                f"{llm_time:.2f}s"
            )