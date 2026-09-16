from __future__ import annotations

import asyncio
import shutil
import uuid
from pathlib import Path
from typing import Any

from fastapi import APIRouter, File, HTTPException, UploadFile

from configs.config import RAW_DATA_DIR
from configs.logging_config import logger
from pipeline.ingest_pipeline import IngestPipeline
from utils.file_utils import validate_upload_file

router = APIRouter(prefix="/upload", tags=["upload"])


async def _run_ingestion(file_paths: list[str], content_types: list[str | None]) -> list[dict[str, Any]]:
    """Run ingestion in a background-friendly async wrapper."""

    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, lambda: IngestPipeline().run(file_paths, content_types))


@router.post("/files")
async def upload_files(files: list[UploadFile] = File(...)) -> dict[str, Any]:
    """Upload one or more documents and ingest them into the local pipeline."""

    if not files:
        raise HTTPException(status_code=400, detail="At least one file must be provided.")

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    saved_paths: list[str] = []
    content_types: list[str | None] = []
    for upload in files:
        if upload.filename is None:
            continue

        try:
            validate_upload_file(upload.filename, upload.content_type)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        destination = RAW_DATA_DIR / f"{uuid.uuid4().hex}_{upload.filename}"
        with destination.open("wb") as buffer:
            shutil.copyfileobj(upload.file, buffer)
        saved_paths.append(str(destination))
        content_types.append(upload.content_type)

    if not saved_paths:
        raise HTTPException(status_code=400, detail="No valid files were uploaded.")

    ingested = await _run_ingestion(saved_paths, content_types)

    return {
        "message": "Files uploaded successfully",
        "files": saved_paths,
        "ingested_documents": ingested,
    }
