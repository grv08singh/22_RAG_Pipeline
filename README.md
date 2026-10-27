# RAG Pipeline

A Retrieval-Augmented Generation (RAG) system for document Q&A, built with LangChain, ChromaDB, and Google Gemini.

## Project Structure

```
22_RAG_Pipeline/
├── config/                 # Configuration files (future use)
├── data/
│   ├── raw/                # Input documents (PDFs)
│   ├── processed/          # Processed chunks (future use)
│   └── embeddings/         # Vector database (ChromaDB)
├── notebooks/              # Jupyter notebooks for exploration
├── scripts/
│   └── cli.py              # CLI entry point
├── src/
│   ├── __init__.py         # Package exports
│   ├── config.py           # Centralized configuration
│   ├── ingest.py           # Document ingestion pipeline
│   ├── retriever.py        # Vector store retrieval
│   ├── generator.py        # LLM response generation
│   ├── rag_pipeline.py     # Main RAG pipeline orchestration
│   └── utils/
│       ├── __init__.py
│       └── logging.py      # Structured logging
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   └── test_logging.py
├── RAG_Project_Assessment.md
├── requirements.txt
└── README.md
```

## Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY="your-gemini-api-key"
```

## Usage

### Using the CLI (Recommended)

```bash
# Ingest the PDF document
python scripts/cli.py ingest

# Test retrieval
python scripts/cli.py retrieve --query "What is the main topic?"

# Run full RAG pipeline
python scripts/cli.py query --query "What is the main philosophical subject?"
```

### Using Python Directly

```python
from src import ingest_pdf, run_rag_pipeline

# Ingest document (run once)
ingest_pdf()

# Run queries
answer = run_rag_pipeline("What is the main topic?")
print(answer)
```

### Using Individual Modules

```python
from src import get_retriever, generate_response

# Get retriever
retriever = get_retriever(k=5)
docs = retriever.invoke("Your query")

# Generate response
context = [doc.page_content for doc in docs]
response = generate_response("Your query", context)
```

## Configuration

All configuration is centralized in `src/config.py` using a `Settings` dataclass. Key settings:

- **Paths**: `PROJECT_ROOT`, `DATA_DIR`, `RAW_DATA_DIR`, `PROCESSED_DATA_DIR`, `EMBEDDINGS_DIR`
- **PDF**: `PDF_FILENAME`, `PDF_PATH`
- **Chunking**: `CHUNK_SIZE`, `CHUNK_OVERLAP`
- **Embeddings**: `EMBEDDING_MODEL_NAME` (default: `all-MiniLM-L6-v2`)
- **Vector Store**: `CHROMA_PATH`, `COLLECTION_NAME`
- **LLM**: `MODEL_NAME` (default: `gemini-flash-lite`), `GEMINI_API_KEY` (from env)
- **Retrieval**: `DEFAULT_TOP_K`
- **Prompt**: `SYSTEM_PROMPT`

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=src --cov-report=term-missing
```

## Architecture

The pipeline follows a modular architecture:

1. **Ingestion** (`ingest.py`): Load PDF → Split into chunks → Generate embeddings → Store in ChromaDB
2. **Retrieval** (`retriever.py`): Load ChromaDB → Query vector store → Return top-K documents
3. **Generation** (`generator.py`): Format context + query → Call Gemini API → Return response
4. **Pipeline** (`rag_pipeline.py`): Orchestrate retrieval + generation

## Future Improvements

See `RAG_Project_Assessment.md` for the complete roadmap to industry-grade system:

- Production robustness (logging, error handling, testing)
- Scalability (distributed processing, managed vector DB)
- Retrieval quality (hybrid search, re-ranking, query augmentation)
- Evaluation (RAGAS, faithfulness metrics, versioning)