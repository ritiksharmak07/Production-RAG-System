import os
import sys
from pathlib import Path

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingestion.loader import DocumentLoader
from pipeline.preprocessing_pipeline import PreprocessingPipeline
from chunking.chunk_manager import ChunkManager

loader = DocumentLoader()

preprocessor = PreprocessingPipeline()

documents = loader.load(
    "data/raw/txt/python.txt"
)

documents = preprocessor.process(
    documents
)

chunk_manager = ChunkManager(
    strategy="recursive"
)

chunks = chunk_manager.create_chunks(
    documents
)

for chunk in chunks:

    print("="*60)

    print(chunk.metadata)

    print(chunk.text)