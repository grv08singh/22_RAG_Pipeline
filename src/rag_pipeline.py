import os
from src.retriever import get_retriever
from src.generator import generate_response
from typing import List

def run_rag_pipeline(user_query: str, top_k: int = 4) -> str:
    """
    Executes the full RAG pipeline: Retrieve context, then generate answer.
    """
    print("--- 🚀 Starting RAG Pipeline ---")
    try:
        # 1. Retrieval
        retriever = get_retriever(k=top_k)
        print(f"Retrieving top {top_k} relevant documents for query: '{user_query}'...")
        retrieved_docs = retriever.invoke(user_query)

        # Extract page_content as strings for the LLM context
        retrieved_context = [doc.page_content for doc in retrieved_docs]

        if not retrieved_context:
            return "Could not retrieve any relevant context from the document."

        print(f"✅ Retrieval successful. {len(retrieved_context)} chunks found.")

        # 2. Generation
        print("🧠 Generating response using Claude Opus 5.5...")
        response = generate_response(user_query, retrieved_context)

        return "\n\n========================================\n" + response + "\n========================================\n"

    except FileNotFoundError as e:
        return f"\n❌ Error: {e}. Please ensure the PDF has been ingested first (run src/ingest.py).\n"
    except Exception as e:
        return f"\n❌ An unexpected error occurred during the RAG pipeline: {e}\n"

if __name__ == "__main__":
    # --- Setup Instructions ---
    # 1. Ensure ANTHROPIC_API_KEY environment variable is set.
    # 2. Run: python src/ingest.py (if not already done)
    # 3. Run: python src/rag_pipeline.py

    # Example usage:
    query = "What is the main philosophical subject of this PDF?"

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("WARNING: ANTHROPIC_API_KEY environment variable is not set. The pipeline will fail at the generation step.")
        print("Please set the API key before running the pipeline.")

    # Execute the pipeline
    final_answer = run_rag_pipeline(query, top_k=5)

    print(final_answer)