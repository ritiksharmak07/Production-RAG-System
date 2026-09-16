from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import AppDependencies, create_app_dependencies
from api.schemas.ask_schema import AskRequest, AskResponse
from configs.logging_config import logger
from utils.search_result import SearchResult

router = APIRouter(prefix="/ask", tags=["ask"])


def get_dependencies() -> AppDependencies:
    return create_app_dependencies()


def build_prompt(query: str, results: list[SearchResult]) -> str:
    context = "\n\n".join(
        f"Source {idx + 1}: {result.chunk.text}" for idx, result in enumerate(results)
    )

    return (
        "You are a helpful assistant. Use the provided context to answer the question.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {query}\n\n"
        "Answer:"
    )


@router.post("/", response_model=AskResponse)
def ask(
    request: AskRequest,
    dependencies: AppDependencies = Depends(get_dependencies),
) -> AskResponse:
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query must not be empty.")

    try:
        query_embedding = dependencies.embedding_generator.generate_query_embedding(request.query)
        search_results = dependencies.faiss_manager.search(query_embedding, top_k=request.top_k)
    except Exception as exc:
        logger.exception("Retrieval failed during ask request")
        raise HTTPException(status_code=500, detail="Retrieval failed") from exc

    if not search_results:
        raise HTTPException(status_code=404, detail="No relevant documents found.")

    try:
        ranked_results = dependencies.reranker.rerank(request.query, search_results, top_k=request.top_k)
        prompt = build_prompt(request.query, ranked_results)
        answer = dependencies.gemini_client.generate(prompt=prompt, max_tokens=512)
    except Exception as exc:
        logger.exception("Answer generation failed")
        raise HTTPException(status_code=500, detail="Answer generation failed") from exc

    sources = [
        result.chunk.metadata.get("filename", f"source_{idx + 1}")
        for idx, result in enumerate(ranked_results)
    ]

    return AskResponse(
        query=request.query,
        answer=answer,
        sources=sources,
    )
