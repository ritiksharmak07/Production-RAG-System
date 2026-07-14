import sys
import os
from pathlib import Path

# Add project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ingestion.loader import DocumentLoader
from pipeline.preprocessing_pipeline import PreprocessingPipeline


def main():
    """
    Main function to test the preprocessing pipeline.
    """
    loader = DocumentLoader()
    pipeline = PreprocessingPipeline()

    # Construct an absolute path to the sample file
    sample_path = Path(__file__).resolve().parent.parent / "data" / "raw" / "txt" / "python.txt"
    documents = loader.load(str(sample_path))

    processed_documents = pipeline.process(documents)

    for doc in processed_documents:
        print(doc.metadata)
        print(doc.text[:200] + "..." if len(doc.text) > 200 else doc.text)
        print("=" * 80)

if __name__ == "__main__":
    main()