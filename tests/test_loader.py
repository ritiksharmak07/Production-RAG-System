import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ingestion.loader import DocumentLoader

def main():
    loader = DocumentLoader()
    sample_path = Path(__file__).resolve().parent.parent / "data" / "raw" / "txt" / "python.txt"
    documents = loader.load(str(sample_path))

    for document in documents:
        print(document.metadata)
        print(document.text[:100])
        print("=" * 60)


if __name__ == "__main__":
    main()