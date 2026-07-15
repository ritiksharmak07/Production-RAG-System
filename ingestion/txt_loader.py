from pathlib import Path
from utils.document import Document


class TXTLoader:

    def load(self, file_path: str):

        file_path = Path(file_path)

        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()

        document = Document(
            text=text,
            metadata={
                "filename": file_path.name,
                "filepath": str(file_path),
                "source": "txt"
            }
        )

        return [document]