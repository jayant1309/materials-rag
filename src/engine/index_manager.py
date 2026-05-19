import chromadb
from llama_index.core import VectorStoreIndex, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.llms.gemini import Gemini

from src.config import settings, Provider
from src.utils.logger import logger


class IndexManager:
    """Manages the creation and loading of the VectorStoreIndex with ChromaDB."""

    def __init__(self):
        self.db_path = settings.storage.chroma_db_path
        self.collection_name = "materials_science_rag"
        self._setup_models()

    def _setup_models(self):
        """Initializes LLM and Embedding models based on the provider settings."""
        # Setup LLM
        if settings.llm.provider == Provider.API:
            logger.info(f"Using API-based LLM: {settings.llm.api_model}")
            Settings.llm = Gemini(
                model=settings.llm.api_model,
                api_key=settings.llm.api_key,
                temperature=settings.llm.temperature
            )
        else:
            logger.info(f"Using Local LLM (Ollama): {settings.llm.model}")
            Settings.llm = Ollama(
                model=settings.llm.model,
                base_url=settings.llm.base_url,
                request_timeout=settings.llm.request_timeout,
                temperature=settings.llm.temperature
            )

        # Setup Embedding
        if settings.embedding.provider == Provider.API:
            logger.info(f"Using API-based Embeddings: {settings.embedding.api_model}")
            Settings.embed_model = GeminiEmbedding(
                model_name=settings.embedding.api_model,
                api_key=settings.embedding.api_key
            )
        else:
            logger.info(f"Using Local Embeddings: {settings.embedding.model_name}")
            Settings.embed_model = HuggingFaceEmbedding(
                model_name=settings.embedding.model_name,
                device=settings.embedding.device
            )

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
