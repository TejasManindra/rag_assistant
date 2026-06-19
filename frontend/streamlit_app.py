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
from backend.vector_store import store_chunks
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
    """
Upload one or more PDFs, process them,
and ask questions across all documents.
"""
)

# =========================
# SESSION STATE
# =========================

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if st.button("🗑 Clear Chat"):

    st.session_state.chat_history = []

    st.success(
        "Chat history cleared."
    )
# =========================
# PDF UPLOAD
# =========================

uploaded_files = st.file_uploader(
    "Upload PDFs",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    st.success(
        f"{len(uploaded_files)} PDF(s) selected"
    )

    for file in uploaded_files:
        st.write(f"📄 {file.name}")

    if st.button("🚀 Process PDFs"):

        with st.spinner("Processing PDFs..."):

            total_chunks = 0

            start_time = time.time()

            for uploaded_file in uploaded_files:

                st.write(
                    f"Processing: {uploaded_file.name}"
                )

                os.makedirs(
                    "uploads",
                    exist_ok=True
                )

                pdf_path = os.path.join(
                    "uploads",
                    uploaded_file.name
                )

                with open(
                    pdf_path,
                    "wb"
                ) as f:
                    f.write(
                        uploaded_file.getbuffer()
                    )

                # Extract text
                text = extract_text(
                    pdf_path
                )

                if len(text.strip()) == 0:
                    st.warning(
                        f"No text found in {uploaded_file.name}"
                    )
                    continue

                # Create chunks
                chunks = create_chunks(
                    text
                )

                if len(chunks) == 0:
                    st.warning(
                        f"No chunks created for {uploaded_file.name}"
                    )
                    continue

                # Generate embeddings
                embeddings = get_embeddings(
                    chunks
                )

                if len(embeddings) == 0:
                    st.warning(
                        f"Embeddings failed for {uploaded_file.name}"
                    )
                    continue

                # Store in ChromaDB
                store_chunks(
                    chunks,
                    embeddings,
                    uploaded_file.name
                )

                total_chunks += len(chunks)

            processing_time = (
                time.time() - start_time
            )

            st.session_state.pdf_processed = True

            st.success(
                f"✅ Processed {len(uploaded_files)} PDFs"
            )

            st.info(
                f"Total Chunks: {total_chunks}"
            )

            st.info(
                f"Processing Time: {processing_time:.2f}s"
            )

# =========================
# QUESTION ANSWERING
# =========================

st.divider()

question = st.text_input(
    "Ask a question about the uploaded documents"
)

if question:

    if not st.session_state.pdf_processed:

        st.warning(
            "⚠️ Please upload and process PDFs first."
        )

    else:

        with st.spinner(
            "Searching documents and generating answer..."
        ):

            # Retrieval
            start = time.time()

            results = retrieve(question)

            retrieval_time = (
                time.time() - start
            )

            docs = results["documents"][0]

            metadata = results.get(
                "metadatas",
                [[]]
            )[0]

            context = "\n".join(
                docs[:4]
            )

            # Build Chat History
            history_text = ""

            for q, a in st.session_state.chat_history:

                history_text += (
                    f"User: {q}\n"
                    f"Assistant: {a}\n\n"
                )

            # LLM
            start = time.time()

            answer = generate_answer(
                question,
                context,
                history_text
            )

            llm_time = (
                time.time() - start
            )

            # Save Conversation
            if len(st.session_state.chat_history) >= 5:
                st.session_state.chat_history.pop(0)


            st.session_state.chat_history.append(
                (question, answer)
            )

        # =========================
        # ANSWER
        # =========================

        st.subheader("📌 Answer")

        st.write(answer)

        # =========================
        # CHAT HISTORY
        # =========================

        with st.expander(
            "💬 Chat History"
        ):

            for q, a in reversed(
                st.session_state.chat_history[-5:]
            ):

                st.markdown(
                    f"**You:** {q}"
                )

                st.markdown(
                    f"**AI:** {a}"
                )

                st.divider()

        # =========================
        # SOURCES
        # =========================

        with st.expander(
            "📚 Retrieved Sources"
        ):

            for i, doc in enumerate(
                docs[:4],
                start=1
            ):

                source_name = "Unknown"

                try:

                    if len(metadata) >= i:

                        meta = metadata[i - 1]

                        if (
                            meta is not None
                            and isinstance(meta, dict)
                        ):
                            source_name = meta.get(
                                "source",
                                "Unknown"
                            )

                except Exception:
                    pass

                st.markdown(
                    f"### Source {i}"
                )

                st.caption(
                    f"📄 {source_name}"
                )

                st.write(doc)

                st.divider()

        # =========================
        # METRICS
        # =========================

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