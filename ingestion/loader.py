from pathlib import Path

from ingestion.pdf_loader import PDFLoader
from ingestion.txt_loader import TXTLoader
from ingestion.docx_loader import DOCXLoader
from ingestion.csv_loader import CSVLoader


class DocumentLoader:

    def __init__(self):

        self.loaders = {

            ".pdf": PDFLoader(),

            ".txt": TXTLoader(),

            ".docx": DOCXLoader(),

            ".csv": CSVLoader()

        }

    def load(self, file_path):

        extension = Path(file_path).suffix.lower()

        if extension not in self.loaders:

            raise ValueError(
                f"Unsupported file type {extension}"
            )

        return self.loaders[extension].load(file_path)