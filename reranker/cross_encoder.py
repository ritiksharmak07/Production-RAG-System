from sentence_transformers import CrossEncoder


class CrossEncoderModel:

    def __init__(
        self,
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):

        print("Loading CrossEncoder...")

        self.model = None
        try:
            self.model = CrossEncoder(model_name)
        except Exception as exc:
            print(f"CrossEncoder unavailable, falling back to original order: {exc}")

    def rerank(
        self,
        query,
        search_results
    ):

        if self.model is None:
            return search_results

        pairs = [

            (
                query,
                result.chunk.text
            )

            for result in search_results

        ]

        scores = self.model.predict(pairs)

        for result, score in zip(
            search_results,
            scores
        ):

            result.score = float(score)

        search_results.sort(

            key=lambda x: x.score,

            reverse=True

        )

        return search_results