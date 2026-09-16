from __future__ import annotations

from fastapi import APIRouter, Request

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Simple health endpoint for liveness checks."""

    return {"status": "ok"}


@router.get("/health/live")
def liveness() -> dict[str, str]:
    return {"status": "ok", "service": "rag-api"}


@router.get("/health/ready")
def readiness(request: Request) -> dict[str, str | bool]:
    dependencies_ready = getattr(request.app.state, "dependencies", None) is not None
    return {
        "status": "ready" if dependencies_ready else "starting",
        "dependencies_loaded": bool(dependencies_ready),
        "service": "rag-api",
    }


@router.get("/metrics")
def metrics(request: Request) -> dict[str, object]:
    metrics_store = getattr(request.app.state, "metrics", {})
    return {
        "service": "rag-api",
        "requests": metrics_store.get("requests", 0),
        "errors": metrics_store.get("errors", 0),
    }
