from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from configs.config import CHUNK_DIR, EMBEDDING_DIR

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".docx", ".csv"}


def validate_upload_file(file_name: str | None, content_type: str | None = None) -> tuple[Path, str]:
    """Validate that the uploaded file is supported and safe to process."""

    if not file_name:
        raise ValueError("Uploaded file is missing a filename")

    suffix = Path(file_name).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file type: {suffix}")

    if content_type and content_type.startswith("application/") and "octet-stream" not in content_type:
        return Path(file_name), content_type

    return Path(file_name), content_type or "application/octet-stream"


def persist_upload_file(source_path: Path, destination_dir: Path) -> Path:
    """Persist an uploaded file to disk and return the stored path."""

    destination_dir.mkdir(parents=True, exist_ok=True)
    destination_path = destination_dir / source_path.name
    shutil.copyfile(source_path, destination_path)
    return destination_path


def write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write JSON payload to disk atomically."""

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)


def persist_chunks(chunks: list[Any], base_name: str) -> Path:
    """Serialize chunks to JSON for later inspection and reprocessing."""

    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    output_path = CHUNK_DIR / f"{base_name}.json"
    payload = [
        {
            "text": chunk.text,
            "metadata": chunk.metadata,
        }
        for chunk in chunks
    ]
    write_json(output_path, {"chunks": payload})
    return output_path


def persist_embeddings(embeddings: Any, base_name: str) -> Path:
    """Persist embeddings to disk as a numpy array payload."""

    EMBEDDING_DIR.mkdir(parents=True, exist_ok=True)
    output_path = EMBEDDING_DIR / f"{base_name}.npy"
    import numpy as np

    np.save(output_path, embeddings)
    return output_path
