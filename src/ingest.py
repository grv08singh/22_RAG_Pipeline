import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from pathlib import Path

# Configuration
PDF_PATH = Path("src/Brihat Parasara Hora Sastra with English Translation Girish Chand Sharma Volume 1.pdf")
CHROMA_PATH = "embeddings"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def ingest_pdf():
    """
    Loads PDF, splits into chunks, generates embeddings, and persists to ChromaDB.
    """
    if not PDF_PATH.exists():
        print(f"Error: PDF not found at {PDF_PATH}")
        return

    print(f"Loading document from {PDF_PATH}...")
    # 1. Load Document
    loader = PyPDFLoader(str(PDF_PATH))
    documents = loader.load()

    print(f"Document loaded with {len(documents)} pages/splits.")

    # 2. Split Text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Text split into {len(chunks)} chunks.")

    # 3. Initialize Embeddings
    # Using a local sentence transformer model for portability
    model_name = "all-MiniLM-L6-v2"
    print(f"Initializing embeddings using {model_name}...")
    embeddings = SentenceTransformerEmbeddings(model_name=model_name)

    # 4. Persist to ChromaDB
    print(f"Creating and persisting ChromaDB vector store at {CHROMA_PATH}...")
    # Chroma will create the directory if it doesn't exist
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    db.persist()
    print("Ingestion complete. Vector store saved.")

if __name__ == "__main__":
    # Ensure the embeddings directory exists
    os.makedirs(CHROMA_PATH, exist_ok=True)
    ingest_pdf()