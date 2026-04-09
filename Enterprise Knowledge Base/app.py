import logging
import streamlit as st

from rag.pipeline import get_rag_pipeline, process_query, RAGResponse
from utils.config import get_config

# -------------------- Logging --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="Enterprise Knowledge Base",
    page_icon="📘",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------- Session State --------------------
def initialize_session_state():
    if "config" not in st.session_state:
        st.session_state.config = get_config()

    if "pipeline" not in st.session_state:
        st.session_state.pipeline = get_rag_pipeline()

    if "recent_queries" not in st.session_state:
        st.session_state.recent_queries = []

    if "last_query" not in st.session_state:
        st.session_state.last_query = ""

    if "last_response" not in st.session_state:
        st.session_state.last_response = None


# -------------------- Minimal CSS --------------------
def apply_custom_css():
    st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 850px;
        }

        .main-title {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
        }

        .sub-text {
            color: #6b7280;
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
        }

        .answer-box {
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 1rem;
            margin-top: 1rem;
            margin-bottom: 1rem;
        }

        .citation-box {
            background: #fafafa;
            border: 1px solid #e5e7eb;
            border-radius: 10px;
            padding: 0.8rem;
            margin-bottom: 0.7rem;
        }

        .footer-text {
            text-align: center;
            color: #9ca3af;
            font-size: 0.85rem;
            margin-top: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)


# -------------------- Header --------------------
def display_header():
    st.markdown('<div class="main-title">📘 Enterprise Knowledge Base</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-text">Ask questions about your documents and get clear answers with citations.</div>',
        unsafe_allow_html=True
    )


# -------------------- Query Form --------------------
def display_query_form():
    with st.form("query_form", clear_on_submit=False):
        user_query = st.text_area(
            "Ask a question",
            value=st.session_state.last_query,
            placeholder="e.g. What are our policies on remote work?",
            height=110
        )

        col1, col2 = st.columns([4, 1])

        with col1:
            submitted = st.form_submit_button("Ask", type="primary", use_container_width=True)

        with col2:
            clear = st.form_submit_button("Clear", use_container_width=True)

        if clear:
            st.session_state.last_query = ""
            st.session_state.last_response = None
            st.rerun()

        if submitted and user_query.strip():
            return user_query.strip()

    return None


# -------------------- Response --------------------
def display_citations(citations):
    if not citations:
        return

    st.markdown("### Citations")
    for citation in citations:
        source = citation.get("source", "Unknown")
        display_source = source.split("/")[-1] if "/" in source else source
        title = citation.get("title", "Untitled")
        index = citation.get("index", "?")

        st.markdown(
            f"""
            <div class="citation-box">
                <strong>[{index}] {title}</strong><br>
                <small>Source: {display_source}</small>
            </div>
            """,
            unsafe_allow_html=True
        )


def display_source_documents(source_documents):
    if not source_documents:
        return

    with st.expander("Source Documents"):
        for i, doc in enumerate(source_documents[:3], 1):
            preview = doc.content[:350] + "..." if len(doc.content) > 350 else doc.content
            st.markdown(f"**{i}. {doc.document_title}**")
            st.caption(f"Score: {doc.score:.3f} | Chunk: #{doc.chunk_index}")
            st.code(preview, language="text")


def display_response(response: RAGResponse):
    if not response.query:
        st.error(response.answer)
        return

    st.markdown("### Answer")
    st.markdown(f'<div class="answer-box">{response.answer}</div>', unsafe_allow_html=True)

    display_citations(response.citations)
    display_source_documents(response.source_documents)


# -------------------- Main --------------------
def main():
    initialize_session_state()
    apply_custom_css()
    display_header()

    user_query = display_query_form()

    if user_query:
        with st.spinner("Generating answer..."):
            try:
                response = process_query(
                    query=user_query,
                    top_k=st.session_state.config.top_k
                )

                st.session_state.last_response = response
                st.session_state.last_query = user_query

                if user_query not in st.session_state.recent_queries:
                    st.session_state.recent_queries.append(user_query)

                display_response(response)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                logger.error(f"Error processing query: {e}")

    elif st.session_state.get("last_response"):
        display_response(st.session_state.last_response)

    st.markdown(
        '<div class="footer-text">Powered by Amazon Bedrock</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()