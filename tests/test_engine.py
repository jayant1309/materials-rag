import pytest
from unittest.mock import MagicMock, patch
from src.engine.query_engine import MaterialsRAGQueryEngine, QueryResult

@pytest.fixture
def mock_index_manager():
    with patch("src.engine.query_engine.IndexManager") as mock:
        instance = mock.return_value
        mock_index = MagicMock()
        
        # Mock a source node
        mock_node = MagicMock()
        mock_node.node.node_id = "test_id"
        mock_node.node.get_content.return_value = "source text"
        mock_node.node.metadata = {"file": "test.pdf"}
        mock_node.score = 0.9
        
        # Mock query engine response
        mock_response = MagicMock()
        mock_response.source_nodes = [mock_node]
        mock_response.__str__.return_value = "Extracted answer"
        
        mock_query_engine = MagicMock()
        mock_query_engine.query.return_value = mock_response
        
        mock_index.as_query_engine.return_value = mock_query_engine
        instance.get_index.return_value = mock_index
        yield instance

def test_query_engine_init(mock_index_manager):
    engine = MaterialsRAGQueryEngine()
    assert engine.query_engine is not None

def test_query_execution(mock_index_manager):
    engine = MaterialsRAGQueryEngine()
    result = engine.query("What is RAM?")
    
    assert isinstance(result, QueryResult)
    assert result.response == "Extracted answer"
    assert len(result.source_nodes) == 1
    assert result.source_nodes[0].node_id == "test_id"
    assert result.source_nodes[0].score == 0.9
