from utils.chunk import Chunk


class RecursiveChunker:

    def __init__(self,
                 chunk_size=500,
                 overlap=100):

        self.chunk_size = chunk_size
        self.overlap = overlap

        self.separators = [
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]

    def split(self, document):

        chunks = self._recursive_split(
            document.text,
            self.separators
        )

        chunk_objects = []

        for i, chunk in enumerate(chunks):

            metadata = document.metadata.copy()

            metadata["chunk_id"] = i

            chunk_objects.append(

                Chunk(
                    text=chunk.strip(),
                    metadata=metadata
                )

            )

        return chunk_objects

    def _recursive_split(
            self,
            text,
            separators):

        if len(text) <= self.chunk_size:
            return [text]

        if not separators:
            return [
                text[i:i+self.chunk_size]
                for i in range(
                    0,
                    len(text),
                    self.chunk_size-self.overlap
                )
            ]

        separator = separators[0]

        if separator == "":
            return [
                text[i:i+self.chunk_size]
                for i in range(
                    0,
                    len(text),
                    self.chunk_size-self.overlap
                )
            ]

        parts = text.split(separator)

        chunks = []

        current = ""

        for part in parts:

            candidate = (
                current
                + separator
                + part
                if current
                else part
            )

            if len(candidate) <= self.chunk_size:

                current = candidate

            else:

                if current:

                    chunks.append(current)

                if len(part) > self.chunk_size:

                    chunks.extend(
                        self._recursive_split(
                            part,
                            separators[1:]
                        )
                    )

                    current = ""

                else:

                    current = part

        if current:

            chunks.append(current)

        return chunks