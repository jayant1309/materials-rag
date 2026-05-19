import os
from pathlib import Path
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import yaml


class LLMSettings(BaseSettings):
    """Settings for the Large Language Model (Ollama)."""
    model_config = SettingsConfigDict(extra="allow")
    base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    model: str = Field(default="llama3", alias="OLLAMA_MODEL")
    temperature: float = 0.1
    request_timeout: float = 120.0


class EmbeddingSettings(BaseSettings):
    """Settings for the embedding model."""
    model_config = SettingsConfigDict(extra="allow")
    model_name: str = Field(default="all-MiniLM-L6-v2", alias="EMBEDDING_MODEL_NAME")
    device: str = "cpu"


class StorageSettings(BaseSettings):
    """Settings for vector storage and data paths."""
    model_config = SettingsConfigDict(extra="allow")
    chroma_db_path: str = Field(default="./chroma_db", alias="CHROMA_DB_PATH")
    data_dir: str = Field(default="./data", alias="DATA_DIR")


class AppSettings(BaseSettings):
    """Global application settings combining all sub-settings."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    llm: LLMSettings = Field(default_factory=LLMSettings)
    embedding: EmbeddingSettings = Field(default_factory=EmbeddingSettings)
    storage: StorageSettings = Field(default_factory=StorageSettings)

    project_root: Path = Path(__file__).parent.parent
    log_level: str = "INFO"


def load_config(config_path: Optional[str] = None) -> AppSettings:
    """
    Loads application settings from environment variables and optionally a YAML file.
    Environment variables have higher priority than YAML settings.
    """
    # Load YAML first if it exists
    yaml_data = {}
    if config_path and os.path.exists(config_path):
        with open(config_path, "r") as f:
            yaml_data = yaml.safe_load(f) or {}
    
    # Create settings. Pydantic Settings will load from ENV.
    # We can pass yaml_data as initial values, and ENV will override them if configured.
    # However, to keep it simple with nested models, we can do:
    settings = AppSettings()
    
    # Only apply YAML if not already set by ENV (or just apply YAML then reload ENV)
    # A better way is to let AppSettings handle it, but for now let's manually merge:
    if yaml_data:
        if "llm" in yaml_data:
            for k, v in yaml_data["llm"].items():
                # Check for field name and its alias in environment
                field = LLMSettings.model_fields.get(k)
                alias = field.alias if field else None
                if os.environ.get(k.upper()) is None and (not alias or os.environ.get(alias) is None):
                    setattr(settings.llm, k, v)
        if "embedding" in yaml_data:
            for k, v in yaml_data["embedding"].items():
                field = EmbeddingSettings.model_fields.get(k)
                alias = field.alias if field else None
                if os.environ.get(k.upper()) is None and (not alias or os.environ.get(alias) is None):
                    setattr(settings.embedding, k, v)
        if "storage" in yaml_data:
            for k, v in yaml_data["storage"].items():
                field = StorageSettings.model_fields.get(k)
                alias = field.alias if field else None
                if os.environ.get(k.upper()) is None and (not alias or os.environ.get(alias) is None):
                    setattr(settings.storage, k, v)
        if "log_level" in yaml_data and os.environ.get("LOG_LEVEL") is None:
            settings.log_level = yaml_data["log_level"]
                    
    return settings

# Global settings instance
settings = load_config(str(Path(__file__).parent.parent / "configs" / "config.yaml"))
