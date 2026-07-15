from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer

from configs.model_config import EMBEDDING_MODEL
from utils.chunk import Chunk


class EmbeddingGenerator:
    """
    Generates embeddings using a Sentence Transformer model.
    """

    def __init__(self):
        print(f"Loading embedding model: {EMBEDDING_MODEL}")

        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def generate(
        self,
        texts: List[str],
        batch_size: int = 32
    ) -> np.ndarray:
        """
        Generate embeddings from a list of text strings.

        Parameters:
            texts (List[str]): List of text inputs
            batch_size (int): Batch size for encoding

        Returns:
            np.ndarray: Embedding matrix
        """

        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
        )

        return embeddings

    def generate_chunks(
        self,
        chunks: List[Chunk],
        batch_size: int = 32
    ) -> np.ndarray:
        """
        Generate embeddings for a list of Chunk objects.
        """

        texts = [chunk.text for chunk in chunks]

        embeddings = self.generate(
            texts=texts,
            batch_size=batch_size
        )

        return embeddings

    def generate_query_embedding(
        self,
        query: str
    ) -> np.ndarray:
        """
        Generate embedding for a single query.
        """

        embedding = self.model.encode(
            query,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embedding