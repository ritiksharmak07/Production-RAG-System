from retriever.hybrid_search import HybridRetriever
from reranker.rerank import Reranker
from llm.response_generator import ResponseGenerator


class RAGPipeline:
    """
    Complete Retrieval-Augmented Generation pipeline.
    """

    def __init__(
        self,
        faiss_manager,
        chunks
    ):

        self.retriever = HybridRetriever(
            faiss_manager,
            chunks
        )

        self.reranker = Reranker()

        self.generator = ResponseGenerator()

    def ask(
        self,
        query: str,
        retrieve_top_k: int = 10,
        rerank_top_k: int = 5
    ):

        # Step 1
        retrieved = self.retriever.retrieve(
            query=query,
            top_k=retrieve_top_k
        )

        # Step 2
        reranked = self.reranker.rerank(
            query=query,
            results=retrieved,
            top_k=rerank_top_k
        )

        # Step 3
        answer = self.generator.generate(
            query=query,
            search_results=reranked
        )

        return {

            "question": query,

            "answer": answer,

            "sources": reranked

        }