from pathlib import Path

from pypdf import PdfReader

from utils.document import Document


class PDFLoader:

    def load(self, file_path: str):

        file_path = Path(file_path)

        reader = PdfReader(file_path)

        documents = []

        for page_number, page in enumerate(reader.pages):

            text = page.extract_text()

            if text is None:
                text = ""

            documents.append(

                Document(
                    text=text,
                    metadata={
                        "filename": file_path.name,
                        "filepath": str(file_path),
                        "page": page_number + 1,
                        "source": "pdf"
                    }
                )

            )

        return documents