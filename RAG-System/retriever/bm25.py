from rank_bm25 import BM25Okapi

from utils.chunk import Chunk
from utils.search_result import SearchResult


class BM25Retriever:

    def __init__(self, chunks: list[Chunk]):

        self.chunks = chunks

        corpus = [
            chunk.text.lower().split()
            for chunk in chunks
        ]

        self.bm25 = BM25Okapi(corpus)

    def search(
        self,
        query: str,
        top_k: int = 5
    ):

        tokens = query.lower().split()

        scores = self.bm25.get_scores(tokens)

        ranked = sorted(
            enumerate(scores),
            key=lambda x: x[1],
            reverse=True
        )

        results = []

        for idx, score in ranked[:top_k]:

            results.append(
                SearchResult(
                    score=float(score),
                    chunk=self.chunks[idx],
                    document_id=idx,
                )
            )

        return results