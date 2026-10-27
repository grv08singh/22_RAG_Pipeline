"""
Main RAG Pipeline module.
Executes the full RAG pipeline: Retrieve context, then generate answer.
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.retriever import get_retriever
from src.generator import generate_response
from config import settings
from utils.logging import setup_logging, get_logger

# Setup logging
setup_logging()
logger = get_logger(__name__)


def run_rag_pipeline(user_query: str, top_k: int = None) -> str:
    """
    Executes the full RAG pipeline: Retrieve context, then generate answer.

    Args:
        user_query: The user's question
        top_k: Number of documents to retrieve (default: settings.DEFAULT_TOP_K)

    Returns:
        Generated answer string
    """
    if top_k is None:
        top_k = settings.DEFAULT_TOP_K

    logger.info("--- 🚀 Starting RAG Pipeline ---")
    try:
        # 1. Retrieval
        retriever = get_retriever(k=top_k)
        logger.info(f"Retrieving top {top_k} relevant documents for query: '{user_query}'...")
        retrieved_docs = retriever.invoke(user_query)

        # Extract page_content as strings for the LLM context
        retrieved_context = [doc.page_content for doc in retrieved_docs]

        if not retrieved_context:
            return "Could not retrieve any relevant context from the document."

        logger.info(f"✅ Retrieval successful. {len(retrieved_context)} chunks found.")

        # 2. Generation
        logger.info("🧠 Generating response using Gemini...")
        response = generate_response(user_query, retrieved_context)

        return "\n\n========================================\n" + response + "\n========================================\n"

    except FileNotFoundError as e:
        error_msg = (
            f"\n❌ Error: {e}. "
            "Please ensure the PDF has been ingested first (run src/ingest.py).\n"
        )
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"\n❌ An unexpected error occurred during the RAG pipeline: {e}\n"
        logger.error(error_msg)
        return error_msg


if __name__ == "__main__":
    # --- Setup Instructions ---
    # 1. Ensure GEMINI_API_KEY environment variable is set.
    # 2. Run: python src/ingest.py (if not already done)
    # 3. Run: python src/rag_pipeline.py

    # Example usage:
    query = "What is the main philosophical subject of this PDF?"

    if not settings.GEMINI_API_KEY:
        logger.warning(
            "GEMINI_API_KEY environment variable is not set. "
            "The pipeline will fail at the generation step."
        )
        logger.warning("Please set the API key before running the pipeline.")

    # Execute the pipeline
    final_answer = run_rag_pipeline(query, top_k=5)

    print(final_answer)