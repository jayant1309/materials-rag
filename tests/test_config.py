import pytest
from src.config import AppSettings, load_config
from pathlib import Path

def test_config_load_defaults():
    settings = load_config()
    assert settings.llm.model == "llama3"
    assert settings.embedding.model_name == "all-MiniLM-L6-v2"
    assert settings.storage.data_dir == "./data"

def test_config_env_override(monkeypatch):
    monkeypatch.setenv("OLLAMA_MODEL", "test-model")
    monkeypatch.setenv("CHROMA_DB_PATH", "/tmp/chroma")
    
    # Reload settings to pick up env vars
    settings = load_config()
    assert settings.llm.model == "test-model"
    assert settings.storage.chroma_db_path == "/tmp/chroma"

def test_project_root():
    settings = load_config()
    assert settings.project_root.exists()
    assert (settings.project_root / "src").exists()
