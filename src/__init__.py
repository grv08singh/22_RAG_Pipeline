"""
RAG Pipeline - A Retrieval-Augmented Generation system for document Q&A.
"""

__version__ = "0.1.0"
__author__ = "Grv"

from .config import settings
from .ingest import ingest_pdf
from .retriever import get_retriever, load_vectorstore
from .generator import generate_response
from .rag_pipeline import run_rag_pipeline

__all__ = [
    "settings",
    "ingest_pdf",
    "get_retriever",
    "load_vectorstore",
    "generate_response",
    "run_rag_pipeline",
]