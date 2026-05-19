import chromadb
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

from src.config import settings
from src.utils.logger import logger


class IndexManager:
    """Manages the creation and loading of the VectorStoreIndex with ChromaDB."""

    def __init__(self):
        self.db_path = settings.storage.chroma_db_path
        self.collection_name = "materials_science_rag"
        
        # Initialize embedding model
        self.embed_model = HuggingFaceEmbedding(
            model_name=settings.embedding.model_name,
            device=settings.embedding.device
        )
        
        # Initialize LLM (Ollama)
        self.llm = Ollama(
            model=settings.llm.model,
            base_url=settings.llm.base_url,
            request_timeout=settings.llm.request_timeout,
            temperature=settings.llm.temperature
        )
        
        # Set global settings for LlamaIndex
        from llama_index.core import Settings
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model

    def get_index(self) -> VectorStoreIndex:
        """
        Initializes or loads the VectorStoreIndex from ChromaDB.
        
        Returns:
            The initialized VectorStoreIndex.
        """
        logger.info(f"Initializing ChromaDB at {self.db_path}")
        
        # Initialize ChromaDB client
        db = chromadb.PersistentClient(path=self.db_path)
        chroma_collection = db.get_or_create_collection(self.collection_name)
        
        # Initialize Vector Store
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        # Initialize or Load Index
        try:
            # Attempt to load index from existing storage
            index = VectorStoreIndex.from_vector_store(
                vector_store, storage_context=storage_context
            )
            logger.info("VectorStoreIndex loaded successfully.")
        except Exception as e:
            logger.warning(f"Could not load index, creating a new one: {e}")
            index = VectorStoreIndex.from_documents(
                [], storage_context=storage_context
            )
            
        return index

    def add_documents(self, documents) -> None:
        """
        Adds documents to the index and persists them.
        """
        index = self.get_index()
        for doc in documents:
            index.insert(doc)
        logger.info(f"Added {len(documents)} documents to the index.")
