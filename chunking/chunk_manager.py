from chunking.fixed_chunker import FixedChunker
from chunking.recursive_chunker import RecursiveChunker


class ChunkManager:

    def __init__(self,
                 strategy="recursive"):

        if strategy == "fixed":

            self.chunker = FixedChunker()

        elif strategy == "recursive":

            self.chunker = RecursiveChunker()

        else:

            raise ValueError(
                "Unknown strategy"
            )

    def create_chunks(
            self,
            documents):

        chunks = []

        for document in documents:

            chunks.extend(
                self.chunker.split(document)
            )

        return chunks