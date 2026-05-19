from typing import List, Optional
from pydantic import BaseModel

from llama_index.core import VectorStoreIndex

from src.engine.index_manager import IndexManager
from src.utils.logger import logger


class SourceNode(BaseModel):
    """Represents a source node for a query response."""
    node_id: str
    text: str
    score: float
    metadata: dict


class QueryResult(BaseModel):
    """Structured result of a RAG query."""
    query: str
    response: str
    source_nodes: List[SourceNode]


class MaterialsRAGQueryEngine:
    """Core Query Engine for the Materials Science Research Assistant."""

    def __init__(self, index: Optional[VectorStoreIndex] = None):
        if index is None:
            self.index_manager = IndexManager()
            self.index = self.index_manager.get_index()
        else:
            self.index = index
            
        # Initialize the query engine with citation support
        # This is crucial for scientific research to track back to sources
        self.query_engine = self.index.as_query_engine(
            similarity_top_k=5,
            response_mode="compact", # or "refine" for higher quality but slower
        )
        
    def query(self, query_str: str) -> QueryResult:
        """
        Executes a query against the RAG system.
        
        Args:
            query_str: The user's question.
            
        Returns:
            A QueryResult object containing the response and source citations.
        """
        logger.info(f"Executing query: {query_str}")
        
        response = self.query_engine.query(query_str)
        
        source_nodes = []
        for node in response.source_nodes:
            source_nodes.append(SourceNode(
                node_id=node.node.node_id,
                text=node.node.get_content(),
                score=node.score or 0.0,
                metadata=node.node.metadata
            ))
            
        return QueryResult(
            query=query_str,
            response=str(response),
            source_nodes=source_nodes
        )
