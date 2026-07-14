from embeddings.embedding_generator import EmbeddingGenerator


class Retriever:

    def __init__(self, faiss_manager):

        self.embedding_generator = EmbeddingGenerator()

        self.faiss_manager = faiss_manager

    def retrieve(

        self,

        query: str,

        top_k: int = 5

    ):

        query_embedding = self.embedding_generator.generate_query_embedding(
            query
        )

        results = self.faiss_manager.search(

            query_embedding,

            top_k=top_k

        )

        return results