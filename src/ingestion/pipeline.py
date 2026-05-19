from pathlib import Path
from typing import List, Optional

from llama_index.core import Document, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.ingestion import IngestionPipeline
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from src.config import settings
from src.ingestion.pdf_parser import get_parser
from src.utils.logger import logger


class IngestionManager:
    """Manages the ingestion pipeline from PDF to Vector Store."""

    def __init__(self, parser_type: str = "marker"):
        self.parser = get_parser(parser_type)
        self.embed_model = HuggingFaceEmbedding(
            model_name=settings.embedding.model_name,
            device=settings.embedding.device
        )
        self.node_parser = SentenceSplitter(
            chunk_size=1024,
            chunk_overlap=200
        )

    def process_directory(self, data_dir: Optional[str] = None) -> List[Document]:
        """
        Parses all PDFs in a directory and runs them through the ingestion pipeline.
        
        Args:
            data_dir: Path to the directory containing PDF files.
            
        Returns:
            A list of processed Documents (or Nodes if pipeline is executed).
        """
        dir_path = Path(data_dir or settings.storage.data_dir)
        if not dir_path.exists():
            logger.error(f"Data directory does not exist: {dir_path}")
            return []

        all_documents = []
        pdf_files = list(dir_path.glob("*.pdf"))
        
        logger.info(f"Found {len(pdf_files)} PDF files in {dir_path}")

        for pdf_file in pdf_files:
            docs = self.parser.parse(pdf_file)
            all_documents.extend(docs)

        if not all_documents:
            logger.warning("No documents were parsed.")
            return []

        # Define the pipeline
        pipeline = IngestionPipeline(
            transformations=[
                self.node_parser,
                self.embed_model,
            ]
        )

        # Run transformations
        logger.info("Running ingestion pipeline transformations...")
        nodes = pipeline.run(documents=all_documents)
        
        # Add to index for persistence
        from src.engine.index_manager import IndexManager
        index_manager = IndexManager()
        index = index_manager.get_index()
        index.insert_nodes(nodes)
        
        logger.info(f"Ingestion complete. Generated and persisted {len(nodes)} nodes.")
        
        return all_documents
