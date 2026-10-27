#!/usr/bin/env python
"""
CLI entry point for the RAG Pipeline.
Provides commands for ingestion, retrieval testing, and running the full pipeline.
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.ingest import ingest_pdf
from src.retriever import get_retriever
from src.rag_pipeline import run_rag_pipeline
from config import settings


def cmd_ingest(args):
    """Run document ingestion."""
    print("Starting document ingestion...")
    ingest_pdf()
    print("Ingestion complete.")


def cmd_retrieve(args):
    """Test retrieval with a query."""
    if not args.query:
        print("Error: --query is required for retrieve command")
        sys.exit(1)

    print(f"Testing retrieval with query: '{args.query}'...")
    try:
        retriever = get_retriever(k=args.top_k)
        retrieved_docs = retriever.invoke(args.query)
        print(f"Retrieved {len(retrieved_docs)} documents.")
        for i, doc in enumerate(retrieved_docs):
            print(f"\n--- Document {i+1} ---")
            print(doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)


def cmd_query(args):
    """Run the full RAG pipeline with a query."""
    if not args.query:
        print("Error: --query is required for query command")
        sys.exit(1)

    if not settings.GEMINI_API_KEY:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        print("Please set it before running the query command.")
        sys.exit(1)

    print(f"Running RAG pipeline with query: '{args.query}'...")
    answer = run_rag_pipeline(args.query, top_k=args.top_k)
    print(answer)


def main():
    parser = argparse.ArgumentParser(
        description="RAG Pipeline CLI - Document Q&A System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/cli.py ingest                    # Ingest the PDF document
  python scripts/cli.py retrieve --query "..."    # Test retrieval
  python scripts/cli.py query --query "..."       # Run full RAG pipeline
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest PDF document into vector store")

    # Retrieve command
    retrieve_parser = subparsers.add_parser("retrieve", help="Test document retrieval")
    retrieve_parser.add_argument("--query", "-q", required=True, help="Query to test retrieval")
    retrieve_parser.add_argument("--top-k", "-k", type=int, default=settings.DEFAULT_TOP_K, help="Number of documents to retrieve")

    # Query command
    query_parser = subparsers.add_parser("query", help="Run full RAG pipeline")
    query_parser.add_argument("--query", "-q", required=True, help="Question to ask")
    query_parser.add_argument("--top-k", "-k", type=int, default=settings.DEFAULT_TOP_K, help="Number of documents to retrieve")

    args = parser.parse_args()

    if args.command == "ingest":
        cmd_ingest(args)
    elif args.command == "retrieve":
        cmd_retrieve(args)
    elif args.command == "query":
        cmd_query(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()