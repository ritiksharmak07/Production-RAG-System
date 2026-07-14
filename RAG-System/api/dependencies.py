from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from embeddings.embedding_generator import EmbeddingGenerator
from reranker.rerank import Reranker
from llm.gemini_client import GeminiClient
from vector_store.index_manager import FAISSIndexManager
from configs.config import FAISS_INDEX_DIR
from configs.model_config import EMBEDDING_DIM


@dataclass
class AppDependencies:
    """Shared application services wired once and reused by the API."""

    embedding_generator: EmbeddingGenerator
    faiss_manager: FAISSIndexManager
    reranker: Reranker
    gemini_client: GeminiClient


def create_app_dependencies() -> AppDependencies:
    """Create the API dependency container for the app lifecycle."""

    embedding_generator = EmbeddingGenerator()
    faiss_manager = FAISSIndexManager(embedding_dimension=EMBEDDING_DIM)
    reranker = Reranker()
    gemini_client = GeminiClient()

    try:
        faiss_manager.load(str(FAISS_INDEX_DIR))
    except Exception:
        pass

    return AppDependencies(
        embedding_generator=embedding_generator,
        faiss_manager=faiss_manager,
        reranker=reranker,
        gemini_client=gemini_client,
    )
