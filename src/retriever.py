"""
Retriever module for the RAG Pipeline.
Loads the ChromaDB vector store and provides retrieval functionality.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

from config import settings
from utils.logging import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)


def load_vectorstore() -> Chroma:
    """
    Loads the ChromaDB vector store from the persistent directory.
    """
    if not settings.CHROMA_PATH.exists():
        raise FileNotFoundError(
            f"ChromaDB vector store not found at {settings.CHROMA_PATH}. "
            "Run ingest.py first."
        )

    logger.info(f"Loading vector store from {settings.CHROMA_PATH}...")
    embeddings = SentenceTransformerEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)

    # Chroma.load will load the data from the specified directory
    db = Chroma(
        persist_directory=str(settings.CHROMA_PATH),
        embedding_function=embeddings,
        collection_name=settings.COLLECTION_NAME
    )
    logger.info("Vector store loaded successfully.")
    return db


def get_retriever(k: int = None) -> Chroma:
    """
    Returns a retriever object configured to fetch the top K relevant documents.

    Args:
        k: Number of documents to retrieve (default: settings.DEFAULT_TOP_K)
    """
    if k is None:
        k = settings.DEFAULT_TOP_K

    db = load_vectorstore()
    retriever = db.as_retriever(search_kwargs={"k": k})
    return retriever


if __name__ == "__main__":
    try:
        retriever = get_retriever(k=5)
        # Test retrieval with a generic query
        test_query = "Tell me about the text in the PDF"
        logger.info(f"Testing retrieval with query: '{test_query}'...")
        retrieved_docs = retriever.invoke(test_query)
        logger.info(f"Successfully retrieved {len(retrieved_docs)} documents.")
        if retrieved_docs:
            logger.info("--- First document content snippet ---")
            logger.info(retrieved_docs[0].page_content[:300] + "...")
            logger.info("------------------------------------")
    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred during retrieval test: {e}")