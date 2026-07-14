from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
CHUNK_DIR = BASE_DIR / "data" / "chunks"
EMBEDDING_DIR = BASE_DIR / "data" / "embeddings"

# Vector database
VECTOR_DB_DIR = BASE_DIR / "vector_store"
FAISS_INDEX_DIR = VECTOR_DB_DIR / "faiss_index"

# Logging
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# Default chunk settings
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100