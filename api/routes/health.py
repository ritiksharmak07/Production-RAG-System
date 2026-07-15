from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    """Simple health endpoint for liveness checks."""

    return {"status": "ok"}
