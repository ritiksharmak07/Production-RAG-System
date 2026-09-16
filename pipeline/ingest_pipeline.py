from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from configs.config import FAISS_INDEX_DIR
from configs.logging_config import logger
from ingestion.loader import DocumentLoader
from embeddings.embedding_generator import EmbeddingGenerator
from vector_store.index_manager import FAISSIndexManager
from chunking.recursive_chunker import RecursiveChunker
from utils.chunk import Chunk
from utils.file_utils import persist_chunks, persist_embeddings, validate_upload_file


class IngestPipeline:
    """Ingest documents end to end into the local vector store."""

    def __init__(self) -> None:
        self.loader = DocumentLoader()
        self.chunker = RecursiveChunker()
        self.embedding_generator = EmbeddingGenerator()
        self.faiss_manager = FAISSIndexManager(embedding_dimension=384)

    def _validate_and_prepare(self, file_path: str, content_type: str | None = None) -> tuple[Path, str]:
        path_obj = Path(file_path)
        if not path_obj.exists():
            raise FileNotFoundError(f"File does not exist: {file_path}")
        return validate_upload_file(path_obj.name, content_type)

    def _build_chunk_id(self, text: str, metadata: dict[str, Any]) -> str:
        payload = f"{text}:{metadata.get('filename', '')}:{metadata.get('source', '')}".encode("utf-8")
        return hashlib.sha256(payload).hexdigest()[:16]

    def run(self, file_paths: list[str], content_types: list[str] | None = None) -> list[dict[str, Any]]:
        """Process a list of files and index the resulting chunks."""

        results: list[dict[str, Any]] = []
        chunks: list[Chunk] = []

        for index, file_path in enumerate(file_paths):
            logger.info("Loading document %s", file_path)
            validated_path, _ = self._validate_and_prepare(file_path, content_types[index] if content_types else None)
            documents = self.loader.load(str(validated_path))
            for document in documents:
                chunked = self.chunker.split(document)
                for chunk in chunked:
                    chunk.metadata["source_file"] = Path(file_path).name
                    chunk.metadata["chunk_id"] = self._build_chunk_id(chunk.text, chunk.metadata)
                chunks.extend(chunked)
                results.append({"file": file_path, "chunks": len(chunked)})

        if not chunks:
            return results

        embeddings = self.embedding_generator.generate_chunks(chunks)
        base_name = hashlib.sha256(str(file_paths).encode("utf-8")).hexdigest()[:12]
        persist_chunks(chunks, base_name)
        persist_embeddings(embeddings, base_name)
        self.faiss_manager.add_embeddings(embeddings, chunks)
        self.faiss_manager.save(str(FAISS_INDEX_DIR))

        return results
