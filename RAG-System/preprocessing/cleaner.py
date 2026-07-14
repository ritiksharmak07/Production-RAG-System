import re

class TextCleaner:

    @staticmethod
    def clean(text: str) -> str:
        """
        Clean extracted text while preserving meaning.
        """

        if not text:
            return ""

        # Normalize newlines
        text = text.replace("\r", "\n")

        # Remove multiple blank lines
        text = re.sub(r"\n+", "\n", text)

        # Replace multiple spaces/tabs with one space
        text = re.sub(r"[ \t]+", " ", text)

        # Remove leading/trailing spaces
        text = text.strip()

        return text