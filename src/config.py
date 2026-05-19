import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml


class LLMSettings(BaseSettings):
    """Settings for the Large Language Model (Ollama)."""
    base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    model: str = Field(default="llama3", alias="OLLAMA_MODEL")
    temperature: float = 0.1
    request_timeout: float = 120.0


class EmbeddingSettings(BaseSettings):
    """Settings for the embedding model."""
    model_name: str = Field(default="all-MiniLM-L6-v2", alias="EMBEDDING_MODEL_NAME")
    device: str = "cpu"


class StorageSettings(BaseSettings):
    """Settings for vector storage and data paths."""
    chroma_db_path: str = Field(default="./chroma_db", alias="CHROMA_DB_PATH")
    data_dir: str = Field(default="./data", alias="DATA_DIR")


class AppSettings(BaseSettings):
    """Global application settings combining all sub-settings."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    llm: LLMSettings = LLMSettings()
    embedding: EmbeddingSettings = EmbeddingSettings()
    storage: StorageSettings = StorageSettings()

    project_root: Path = Path(__file__).parent.parent
    log_level: str = "INFO"


def load_config(config_path: Optional[str] = None) -> AppSettings:
    """
    Loads application settings from environment variables and optionally a YAML file.
    
    Args:
        config_path: Optional path to a YAML configuration file.
        
    Returns:
        An instance of AppSettings.
    """
    settings = AppSettings()
    
    if config_path and os.path.exists(config_path):
        with open(config_path, "r") as f:
            yaml_config = yaml.safe_load(f)
            # Update settings with YAML values if they exist
            if yaml_config:
                # Simple update logic for nested Pydantic models
                if "llm" in yaml_config:
                    settings.llm = LLMSettings(**{**settings.llm.model_dump(), **yaml_config["llm"]})
                if "embedding" in yaml_config:
                    settings.embedding = EmbeddingSettings(**{**settings.embedding.model_dump(), **yaml_config["embedding"]})
                if "storage" in yaml_config:
                    settings.storage = StorageSettings(**{**settings.storage.model_dump(), **yaml_config["storage"]})
                if "log_level" in yaml_config:
                    settings.log_level = yaml_config["log_level"]
                    
    return settings

# Global settings instance
settings = load_config(str(Path(__file__).parent.parent / "configs" / "config.yaml"))
