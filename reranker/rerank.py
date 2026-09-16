from reranker.cross_encoder import CrossEncoderModel


class Reranker:

    def __init__(self):

        self.model = CrossEncoderModel()

    def rerank(
        self,
        query,
        results,
        top_k=5
    ):

        ranked = self.model.rerank(
            query,
            results
        )

        return ranked[:top_k]