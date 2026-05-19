import pytest
from unittest.mock import MagicMock, patch
from pathlib import Path
from llama_index.core import Document
from src.ingestion.pipeline import IngestionManager

@pytest.fixture
def mock_parser():
    with patch("src.ingestion.pipeline.get_parser") as mock:
        parser = MagicMock()
        parser.parse.return_value = [Document(text="Test content", metadata={"source": "test.pdf"})]
        mock.return_value = parser
        yield parser

@pytest.fixture
def mock_llm_embed():
    with patch("src.ingestion.pipeline.HuggingFaceEmbedding") as mock_embed:
        mock_embed.return_value = MagicMock()
        yield mock_embed

def test_ingestion_manager_init(mock_parser, mock_llm_embed):
    manager = IngestionManager(parser_type="marker")
    assert manager.parser is not None
    assert manager.embed_model is not None

@patch("src.ingestion.pipeline.IngestionPipeline")
@patch("src.engine.index_manager.IndexManager")
def test_process_directory(mock_idx_mgr, mock_pipeline, mock_parser, mock_llm_embed, tmp_path):
    # Setup tmp directory with a pdf
    d = tmp_path / "data"
    d.mkdir()
    (d / "test.pdf").write_text("dummy")
    
    manager = IngestionManager()
    
    # Mock pipeline run to return dummy nodes
    mock_pipeline_instance = mock_pipeline.return_value
    mock_pipeline_instance.run.return_value = [MagicMock()]
    
    # Mock index manager
    mock_idx_instance = mock_idx_mgr.return_value
    mock_idx_instance.get_index.return_value = MagicMock()
    
    docs = manager.process_directory(data_dir=str(d))
    
    assert len(docs) == 1
    assert docs[0].text == "Test content"
    mock_parser.parse.assert_called_once()
    mock_pipeline_instance.run.assert_called_once()
