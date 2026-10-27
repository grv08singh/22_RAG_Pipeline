Summary of Changes

  Directory Reorganization

  Before:
  22_RAG_Pipeline/
  ├── config/ (empty)
  ├── data/
  │   ├── processed/ (empty)
  │   ├── b0c1653b-6d0b-49c5-9b6b-b8d0446f0ffe/ (duplicate)
  │   └── chroma.sqlite3 (duplicate)
  ├── embeddings/
  │   ├── b0c1653b-6d0b-49c5-9b6b-b8d0446f0ffe/
  │   └── chroma.sqlite3 (actual embeddings)
  ├── notebooks/ (empty)
  ├── src/
  │   ├── generator.py
  │   ├── ingest.py
  │   ├── rag_pipeline.py
  │   └── retriever.py
  ├── tests/ (empty)
  ├── RAG_Project_Assessment.md
  └── requirements.txt

  After:
  22_RAG_Pipeline/
  ├── config/                 # For future config files
  ├── data/
  │   ├── raw/                # PDF document
  │   │   └── Brihat Parasara Hora Sastra with English Translation Girish Chand Sharma Volume 1.pdf
  │   ├── processed/          # For future processed chunks
  │   └── embeddings/         # Vector database (ChromaDB)
  │       ├── b0c1653b-6d0b-49c5-9b6b-b8d0446f0ffe/
  │       └── chroma.sqlite3
  ├── notebooks/              # For Jupyter notebooks
  ├── scripts/
  │   └── cli.py              # CLI entry point
  ├── src/
  │   ├── __init__.py         # Package exports
  │   ├── config.py           # Centralized configuration
  │   ├── ingest.py           # Document ingestion (updated)
  │   ├── retriever.py        # Vector store retrieval (updated)
  │   ├── generator.py        # LLM response generation (updated)
  │   ├── rag_pipeline.py     # Main RAG pipeline (updated)
  │   └── utils/
  │       ├── __init__.py
  │       └── logging.py      # Structured logging
  ├── tests/
  │   ├── __init__.py
  │   ├── test_config.py
  │   └── test_logging.py
  ├── RAG_Project_Assessment.md
  ├── requirements.txt        # Updated with test/dev deps
  └── README.md               # New documentation

  Key Improvements Made

  1. Eliminated duplicate data: Removed duplicate embeddings/ folder and duplicate files in data/ root, consolidated everything under data/embeddings/
  2. Moved PDF to proper location: Moved the PDF from src/ to data/raw/
  3. Created centralized configuration (src/config.py):
     - All paths, model names, and settings in one place
     - Uses pathlib.Path for cross-platform compatibility
     - Automatic directory creation
  4. Added structured logging (src/utils/logging.py):
     - Replaced print() statements with proper logging
     - Configurable levels and formatters
     - Optional file logging support
  5. Updated all source modules to use the new config and logging:
     - ingest.py - Uses settings.PDF_PATH, settings.CHROMA_PATH, etc.
  ├── RAG_Project_Assessment.md
  ├── RAG_Project_Assessment.md
  ├── requirements.txt        # Updated with test/dev deps
  └── README.md               # New documentation

  Key Improvements Made

  1. Eliminated duplicate data: Removed duplicate embeddings/ folder and duplicate files in data/ root, consolidated everything under data/embeddings/
  2. Moved PDF to proper location: Moved the PDF from src/ to data/raw/
  3. Created centralized configuration (src/config.py):
     - All paths, model names, and settings in one place
     - Uses pathlib.Path for cross-platform compatibility
     - Automatic directory creation
  4. Added structured logging (src/utils/logging.py):
     - Replaced print() statements with proper logging
     - Configurable levels and formatters
     - Optional file logging support
  5. Updated all source modules to use the new config and logging:
     - ingest.py - Uses settings.PDF_PATH, settings.CHROMA_PATH, etc.
     - retriever.py - Uses centralized config
     - generator.py - Uses centralized config, proper error handling
     - rag_pipeline.py - Uses centralized config and logging
  6. Created CLI entry point (scripts/cli.py):
     - python scripts/cli.py ingest - Ingest PDF
     - python scripts/cli.py retrieve --query "..." - Test retrieval
     - python scripts/cli.py query --query "..." - Run full pipeline
  7. Added test structure with basic tests for config and logging
  8. Updated requirements.txt with testing and development dependencies
  9. Created comprehensive README.md with usage instructions

  The project is now organized following industry best practices with clear separation of concerns, centralized configuration, proper logging, and a clean directory
  structure.