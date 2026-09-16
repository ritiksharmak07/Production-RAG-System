from utils.chunk import Chunk


class FixedChunker:

    def __init__(self,
                 chunk_size=500,
                 overlap=100):

        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, document):

        words = document.text.split()

        chunks = []

        start = 0

        while start < len(words):

            end = start + self.chunk_size

            chunk_words = words[start:end]

            chunk_text = " ".join(chunk_words)

            metadata = document.metadata.copy()

            metadata["start_word"] = start
            metadata["end_word"] = end

            chunks.append(
                Chunk(
                    text=chunk_text,
                    metadata=metadata
                )
            )

            start += self.chunk_size - self.overlap

        return chunks