import os
from typing import List
import google.genai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration
# It's best practice to load API keys from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-flash-lite"  # Using the requested model
SYSTEM_PROMPT = (
    "You are a helpful, expert Q&A assistant specialized in the provided PDF document. "
    "Answer the user's question STRICTLY based on the context provided below. "
    "If the context does not contain the answer, state clearly that the information is not available in the document. "
    "Do not use external knowledge."
)

def generate_response(user_query: str, retrieved_context: List[str]) -> str:
    """
    Generates a response using the Gemini API based on the query and retrieved context.
    """
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY environment variable is not set. Please set it to run the LLM."

    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        return f"Error initializing Gemini client: {e}"

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
            model=MODEL_NAME,
            contents=[
                {"role": "user", "parts": [SYSTEM_PROMPT, full_prompt]}
            ]
        )
        return response.text
    except APIError as e:
        return f"Gemini API Error: {e}"
    except Exception as e:
        return f"An unexpected error occurred during generation: {e}"

if __name__ == "__main__":
    # Example usage placeholder (requires setting GEMINI_API_KEY)
    if not GEMINI_API_KEY:
        print("Skipping LLM test: Set GEMINI_API_KEY environment variable.")
    else:
        # In a real end-to-end test, we would load retriever and get context here.
        test_query = "What is the primary subject of this PDF?"
        print(f"Running placeholder LLM test for query: '{test_query}'...")
        # Note: Mocking retrieved context as we don't have the retriever initialized here.
        mock_context = ["The document discusses the Brihat Parasara Hora Sastra, a significant text on Hindu astrology and philosophy."]

        response = generate_response(test_query, mock_context)
        print("\n--- LLM Response ---")
        print(response)
        print("--------------------")