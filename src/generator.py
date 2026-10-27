"""
Generator module for the RAG Pipeline.
Generates responses using the Gemini API based on query and retrieved context.
"""

import sys
from pathlib import Path
from typing import List

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

import google.genai as genai
from dotenv import load_dotenv

from config import settings
from utils.logging import setup_logging, get_logger

# Load environment variables from .env file
load_dotenv()

# Setup logging
setup_logging()
logger = get_logger(__name__)


def generate_response(user_query: str, retrieved_context: List[str]) -> str:
    """
    Generates a response using the Gemini API based on the query and retrieved context.

    Args:
        user_query: The user's question
        retrieved_context: List of context strings from retrieved documents

    Returns:
        Generated response string
    """
    if not settings.GEMINI_API_KEY:
        error_msg = (
            "Error: GEMINI_API_KEY environment variable is not set. "
            "Please set it to run the LLM."
        )
        logger.error(error_msg)
        return error_msg

    try:
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
    except Exception as e:
        error_msg = f"Error initializing Gemini client: {e}"
        logger.error(error_msg)
        return error_msg

    context_text = "\n---\n".join(retrieved_context)

    # Construct the content for the model
    full_prompt = f"""
    <context>
    {context_text}
    </context>

    <user_query>
    {user_query}
    </user_query>
    """

    try:
        # Use the chat/generate content endpoint
        response = client.models.generate_content(
            model=settings.MODEL_NAME,
            contents=[
                {"role": "user", "parts": [settings.SYSTEM_PROMPT, full_prompt]}
            ]
        )
        logger.info("Response generated successfully.")
        return response.text
    except genai.APIError as e:
        error_msg = f"Gemini API Error: {e}"
        logger.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"An unexpected error occurred during generation: {e}"
        logger.error(error_msg)
        return error_msg


if __name__ == "__main__":
    # Example usage placeholder (requires setting GEMINI_API_KEY)
    if not settings.GEMINI_API_KEY:
        logger.warning("Skipping LLM test: Set GEMINI_API_KEY environment variable.")
    else:
        # In a real end-to-end test, we would load retriever and get context here.
        test_query = "What is the primary subject of this PDF?"
        logger.info(f"Running placeholder LLM test for query: '{test_query}'...")
        # Note: Mocking retrieved context as we don't have the retriever initialized here.
        mock_context = [
            "The document discusses the Brihat Parasara Hora Sastra, "
            "a significant text on Hindu astrology and philosophy."
        ]

        response = generate_response(test_query, mock_context)
        logger.info("\n--- LLM Response ---")
        logger.info(response)
        logger.info("--------------------")