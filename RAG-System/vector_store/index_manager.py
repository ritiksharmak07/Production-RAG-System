import pickle
from pathlib import Path
from typing import List

import faiss
import numpy as np

from utils.chunk import Chunk
from utils.search_result import SearchResult


class FAISSIndexManager:
    """
    Manages FAISS index creation, searching,
    saving, and loading.
    """

    def __init__(self, embedding_dimension: int):

        self.embedding_dimension = embedding_dimension

        # Using Inner Product because embeddings are normalized.
        self.index = faiss.IndexFlatIP(embedding_dimension)

        # Maps FAISS index -> Chunk
        self.chunk_store: dict[int, Chunk] = {}

    def add_embeddings(
        self,
        embeddings: np.ndarray,
        chunks: List[Chunk]
    ) -> None:
        """
        Add embeddings and corresponding chunks
        into the FAISS index.
        """

        embeddings = np.asarray(
            embeddings,
            dtype=np.float32
        )

        if embeddings.ndim != 2:
            raise ValueError(
                "Embeddings must be a 2D numpy array."
            )

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must match."
            )

        start_index = self.index.ntotal

        self.index.add(embeddings)

        for i, chunk in enumerate(chunks):
            self.chunk_store[start_index + i] = chunk

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5
    ) -> List[SearchResult]:
        """
        Search the FAISS index.
        """

        query_embedding = np.asarray(
            query_embedding,
            dtype=np.float32
        ).reshape(1, -1)

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, idx in zip(scores[0], indices[0]):

            if idx == -1:
                continue

            if idx not in self.chunk_store:
                continue

            chunk = self.chunk_store[idx]
            document_id = chunk.metadata.get("id") if isinstance(chunk.metadata, dict) else None
            if document_id is None:
                document_id = idx

            results.append(
                SearchResult(
                    score=float(score),
                    chunk=chunk,
                    document_id=document_id,
                )
            )

        return results

    def save(
        self,
        directory: str
    ) -> None:
        """
        Save FAISS index and metadata.
        """

        directory = Path(directory)

        directory.mkdir(
            parents=True,
            exist_ok=True
        )

        faiss.write_index(
            self.index,
            str(directory / "index.faiss")
        )

        with open(
            directory / "metadata.pkl",
            "wb"
        ) as file:

            pickle.dump(
                self.chunk_store,
                file
            )

    def load(
        self,
        directory: str
    ) -> None:
        """
        Load FAISS index and metadata.
        """

        directory = Path(directory)

        self.index = faiss.read_index(
            str(directory / "index.faiss")
        )

        with open(
            directory / "metadata.pkl",
            "rb"
        ) as file:

            self.chunk_store = pickle.load(file)

    def total_vectors(self) -> int:
        """
        Returns total vectors in FAISS.
        """

        return self.index.ntotal

    def clear(self) -> None:
        """
        Reset index and metadata.
        """

        self.index = faiss.IndexFlatIP(
            self.embedding_dimension
        )

        self.chunk_store.clear()