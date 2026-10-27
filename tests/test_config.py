"""
Tests for the configuration module.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from config import settings


def test_settings_exist():
    """Test that settings object exists with expected attributes."""
    assert settings is not None
    assert hasattr(settings, 'PROJECT_ROOT')
    assert hasattr(settings, 'DATA_DIR')
    assert hasattr(settings, 'RAW_DATA_DIR')
    assert hasattr(settings, 'PROCESSED_DATA_DIR')
    assert hasattr(settings, 'EMBEDDINGS_DIR')
    assert hasattr(settings, 'PDF_PATH')
    assert hasattr(settings, 'CHROMA_PATH')
    assert hasattr(settings, 'EMBEDDING_MODEL_NAME')
    assert hasattr(settings, 'CHUNK_SIZE')
    assert hasattr(settings, 'CHUNK_OVERLAP')
    assert hasattr(settings, 'DEFAULT_TOP_K')
    assert hasattr(settings, 'MODEL_NAME')
    assert hasattr(settings, 'SYSTEM_PROMPT')


def test_paths_are_pathlib():
    """Test that path attributes are pathlib.Path objects."""
    assert isinstance(settings.PROJECT_ROOT, Path)
    assert isinstance(settings.DATA_DIR, Path)
    assert isinstance(settings.RAW_DATA_DIR, Path)
    assert isinstance(settings.PROCESSED_DATA_DIR, Path)
    assert isinstance(settings.EMBEDDINGS_DIR, Path)
    assert isinstance(settings.PDF_PATH, Path)
    assert isinstance(settings.CHROMA_PATH, Path)


def test_default_values():
    """Test that default values are correct."""
    assert settings.CHUNK_SIZE == 1000
    assert settings.CHUNK_OVERLAP == 200
    assert settings.EMBEDDING_MODEL_NAME == "all-MiniLM-L6-v2"
    assert settings.DEFAULT_TOP_K == 4
    assert settings.MODEL_NAME == "gemini-flash-lite"
    assert settings.COLLECTION_NAME == "rag_documents"


def test_pdf_path_structure():
    """Test that PDF path is correctly structured."""
    assert settings.PDF_PATH.name == settings.PDF_FILENAME
    assert settings.PDF_PATH.parent == settings.RAW_DATA_DIR