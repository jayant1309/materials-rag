import streamlit as st
from pathlib import Path
import os

from src.engine.query_engine import MaterialsRAGQueryEngine
from src.ingestion.pipeline import IngestionManager
from src.config import settings
from src.utils.logger import logger

# Page configuration
st.set_page_config(
    page_title="Materials Science RAG Assistant",
    page_icon="🔬",
    layout="wide"
)

st.title("🔬 Materials Science RAG Assistant")
st.markdown("""
Predict material properties and explore radar absorbing materials with AI-powered research.
""")

# Initialize Session State
if "query_engine" not in st.session_state:
    with st.spinner("Initializing RAG Engine..."):
        try:
            st.session_state.query_engine = MaterialsRAGQueryEngine()
        except Exception as e:
            st.error(f"Failed to initialize RAG Engine: {e}")
            logger.exception(e)

# Sidebar for management
with st.sidebar:
    st.header("Data Management")
    
    # PDF Upload
    uploaded_files = st.file_uploader("Upload Materials Science PDFs", type="pdf", accept_multiple_files=True)
    
    if st.button("Ingest Documents"):
        if uploaded_files:
            # Save uploaded files to data directory
            data_dir = Path(settings.storage.data_dir)
            data_dir.mkdir(parents=True, exist_ok=True)
            
            for uploaded_file in uploaded_files:
                file_path = data_dir / uploaded_file.name
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                st.info(f"Saved: {uploaded_file.name}")
            
            # Run ingestion pipeline
            with st.spinner("Ingesting documents..."):
                try:
                    ingestion_manager = IngestionManager()
                    documents = ingestion_manager.process_directory()
                    # Add to index
                    from src.engine.index_manager import IndexManager
                    idx_mgr = IndexManager()
                    idx_mgr.add_documents(documents)
                    st.success(f"Successfully ingested {len(documents)} documents!")
                    # Refresh query engine
                    st.session_state.query_engine = MaterialsRAGQueryEngine()
                except Exception as e:
                    st.error(f"Ingestion failed: {e}")
                    logger.exception(e)
        else:
            st.warning("Please upload at least one PDF.")

    st.divider()
    st.header("Settings")
    st.write(f"**LLM Model:** {settings.llm.model}")
    st.write(f"**Embedding Model:** {settings.embedding.model_name}")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("View Sources"):
                for source in message["sources"]:
                    st.write(f"**ID:** {source['node_id']} | **Score:** {source['score']:.4f}")
                    st.write(source["text"][:500] + "...")
                    st.json(source["metadata"])

# Chat input
if prompt := st.chat_input("Ask about material properties or radar absorbing materials..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = st.session_state.query_engine.query(prompt)
                st.markdown(result.response)
                
                # Prepare source data for UI
                sources = [
                    {
                        "node_id": s.node_id,
                        "score": s.score,
                        "text": s.text,
                        "metadata": s.metadata
                    }
                    for s in result.source_nodes
                ]
                
                # Add assistant response to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": result.response,
                    "sources": sources
                })
                
                with st.expander("View Sources"):
                    for source in sources:
                        st.write(f"**ID:** {source['node_id']} | **Score:** {source['score']:.4f}")
                        st.write(source["text"][:500] + "...")
                        st.json(source["metadata"])
                        
            except Exception as e:
                st.error(f"An error occurred: {e}")
                logger.exception(e)
