from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query

from api.dependencies import AppDependencies, create_app_dependencies
from configs.logging_config import logger

router = APIRouter(prefix="/search", tags=["search"])


def get_dependencies() -> AppDependencies:
    return create_app_dependencies()


@router.get("/")
def search_documents(
    query: str = Query(..., min_length=1),
    top_k: int = Query(5, ge=1, le=20),
    dependencies: AppDependencies = Depends(get_dependencies),
) -> dict[str, object]:
    """Search the indexed documents using the current retrieval pipeline."""

    try:
        query_embedding = dependencies.embedding_generator.generate_query_embedding(query)
        search_results = dependencies.faiss_manager.search(query_embedding, top_k=top_k)
    except Exception as exc:
        logger.exception("Search failed")
        raise HTTPException(status_code=500, detail="Search failed") from exc

    if not search_results:
        raise HTTPException(status_code=404, detail="No relevant documents found.")

    return {
        "query": query,
        "results": [
            {
                "score": result.score,
                "text": result.chunk.text,
                "source": result.chunk.metadata.get("filename", "unknown"),
            }
            for result in search_results
        ],
    }
