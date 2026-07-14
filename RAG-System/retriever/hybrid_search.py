from retriever.bm25 import BM25Retriever
from retriever.retriever import Retriever


class HybridRetriever:

    def __init__(
        self,
        faiss_manager,
        chunks
    ):

        self.semantic = Retriever(
            faiss_manager
        )

        self.keyword = BM25Retriever(
            chunks
        )

    def retrieve(
        self,
        query,
        top_k=5
    ):

        semantic_results = self.semantic.retrieve(
            query,
            top_k
        )

        keyword_results = self.keyword.search(
            query,
            top_k
        )

        merged = {}

        for result in semantic_results:

            key = id(result.chunk)

            merged[key] = result

        for result in keyword_results:

            key = id(result.chunk)

            if key in merged:

                merged[key].score += result.score

            else:

                merged[key] = result

        results = list(merged.values())

        results.sort(
            key=lambda x: x.score,
            reverse=True
        )

        return results[:top_k]