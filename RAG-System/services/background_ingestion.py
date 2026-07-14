from __future__ import annotations

import asyncio
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from configs.logging_config import logger
from pipeline.ingest_pipeline import IngestPipeline


class BackgroundIngestionService:
    """Simple background ingestion service for production-style document processing."""

    def __init__(self, max_workers: int = 2) -> None:
        self._executor = ThreadPoolExecutor(max_workers=max_workers)
        self._lock = threading.Lock()
        self._tasks: set[asyncio.Future[Any]] = set()

    def submit(self, file_paths: list[str], content_types: list[str | None] | None = None) -> None:
        """Submit ingestion work to the background executor."""

        def _run() -> None:
            try:
                IngestPipeline().run(file_paths, content_types or [])
            except Exception as exc:
                logger.exception("Background ingestion failed")

        self._executor.submit(_run)

    def shutdown(self) -> None:
        """Shut down the executor cleanly."""

        self._executor.shutdown(wait=True)
