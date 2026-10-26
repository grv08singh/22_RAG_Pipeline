import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# Configuration
CHROMA_PATH = "embeddings"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

def load_vectorstore():
    """
    Loads the ChromaDB vector store from the persistent directory.
    """
    if not os.path.exists(CHROMA_PATH):
        raise FileNotFoundError(f"ChromaDB vector store not found at {CHROMA_PATH}. Run ingest.py first.")

    print(f"Loading vector store from {CHROMA_PATH}...")
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    # Chroma.load will load the data from the specified directory
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embeddings)
    print("Vector store loaded successfully.")
    return db

def get_retriever(k: int = 4):
    """
    Returns a retriever object configured to fetch the top K relevant documents.
    """
    db = load_vectorstore()
    # The retriever is a wrapper around the vector store's similarity search
    retriever = db.as_retriever(search_kwargs={"k": k})
    return retriever

if __name__ == "__main__":
    try:
        retriever = get_retriever(k=5)
        # Test retrieval with a generic query
        test_query = "Tell me about the text in the PDF"
        print(f"\nTesting retrieval with query: '{test_query}'...")
        retrieved_docs = retriever.invoke(test_query)
        print(f"Successfully retrieved {len(retrieved_docs)} documents.")
        if retrieved_docs:
            print("--- First document content snippet ---")
            print(retrieved_docs[0].page_content[:300] + "...")
            print("------------------------------------")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during retrieval test: {e}")