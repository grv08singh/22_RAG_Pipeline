"""
Document ingestion module for the RAG Pipeline.
Loads PDF, splits into chunks, generates embeddings, and persists to ChromaDB.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma

from config import settings
from utils.logging import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)


def ingest_pdf() -> None:
    """
    Loads PDF, splits into chunks, generates embeddings, and persists to ChromaDB.
    """
    if not settings.PDF_PATH.exists():
        logger.error(f"PDF not found at {settings.PDF_PATH}")
        return

    logger.info(f"Loading document from {settings.PDF_PATH}...")
    # 1. Load Document
    loader = PyPDFLoader(str(settings.PDF_PATH))
    documents = loader.load()

    logger.info(f"Document loaded with {len(documents)} pages/splits.")

    # 2. Split Text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    logger.info(f"Text split into {len(chunks)} chunks.")

    # 3. Initialize Embeddings
    logger.info(f"Initializing embeddings using {settings.EMBEDDING_MODEL_NAME}...")
    embeddings = SentenceTransformerEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)

    # 4. Persist to ChromaDB
    logger.info(f"Creating and persisting ChromaDB vector store at {settings.CHROMA_PATH}...")
    settings.CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(settings.CHROMA_PATH),
        collection_name=settings.COLLECTION_NAME
    )
    db.persist()
    logger.info("Ingestion complete. Vector store saved.")


if __name__ == "__main__":
    ingest_pdf()