"""
Configuration management for the RAG Pipeline.
Centralizes all paths, model names, and settings.
"""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class Settings:
    """Application settings loaded from environment variables with defaults."""

    # Project paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    RAW_DATA_DIR: Path = DATA_DIR / "raw"
    PROCESSED_DATA_DIR: Path = DATA_DIR / "processed"
    EMBEDDINGS_DIR: Path = DATA_DIR / "embeddings"

    # PDF document
    PDF_FILENAME: str = "Brihat Parasara Hora Sastra with English Translation Girish Chand Sharma Volume 1.pdf"
    PDF_PATH: Path = RAW_DATA_DIR / PDF_FILENAME

    # Chunking settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    # Embedding model
    EMBEDDING_MODEL_NAME: str = "all-MiniLM-L6-v2"

    # Vector store
    CHROMA_PATH: Path = EMBEDDINGS_DIR
    COLLECTION_NAME: str = "rag_documents"

    # LLM settings
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    MODEL_NAME: str = "gemini-flash-lite"

    # Retrieval settings
    DEFAULT_TOP_K: int = 4

    # System prompt
    SYSTEM_PROMPT: str = (
        "You are a helpful, expert Q&A assistant specialized in the provided PDF document. "
        "Answer the user's question STRICTLY based on the context provided below. "
        "If the context does not contain the answer, state clearly that the information is not available in the document. "
        "Do not use external knowledge."
    )

    def __post_init__(self):
        """Validate and create directories if needed."""
        self.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()