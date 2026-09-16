import collections
import logging
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

from api.dependencies import create_app_dependencies
from api.routes.ask import router as ask_router
from api.routes.health import router as health_router
from api.routes.search import router as search_router
from api.routes.upload import router as upload_router
from configs.logging_config import logger
from services.background_ingestion import BackgroundIngestionService


PLACEHOLDER_VALUES = {
    "replace_with_real_api_key",
    "replace_with_real_key_in_runtime_secret_store",
    "your_api_key_here",
    "changeme",
    "example",
    "demo",
}


def get_api_keys() -> set[str]:
    keys: set[str] = set()
    for raw_key in os.getenv("API_KEYS", "").split(","):
        key = raw_key.strip()
        if not key:
            continue
        normalized = key.lower().replace("-", "").replace("_", "")
        if normalized in {value.lower().replace("-", "").replace("_", "") for value in PLACEHOLDER_VALUES}:
            continue
        keys.add(key)
    return keys


def get_allowed_origins() -> list[str]:
    origins: list[str] = []
    for origin in os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(","):
        value = origin.strip()
        if value and value not in {"replace_with_real_origin", "your_origin_here"}:
            origins.append(value)
    return origins


PUBLIC_PATHS = {"/health", "/health/live", "/health/ready", "/metrics", "/docs", "/openapi.json", "/redoc"}


class InMemoryRateLimiter:
    def __init__(self, limit_per_minute: int = 60, window_seconds: int = 60):
        self.limit_per_minute = limit_per_minute
        self.window_seconds = window_seconds
        self.requests: dict[str, collections.deque[float]] = collections.defaultdict(collections.deque)

    def allow(self, client_ip: str) -> bool:
        now = time.monotonic()
        bucket = self.requests[client_ip]
        while bucket and now - bucket[0] > self.window_seconds:
            bucket.popleft()

        if len(bucket) >= self.limit_per_minute:
            return False

        bucket.append(now)
        return True


rate_limiter = InMemoryRateLimiter(limit_per_minute=60, window_seconds=60)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting RAG API application")
    app.state.dependencies = create_app_dependencies()
    app.state.background_ingestion = BackgroundIngestionService()
    app.state.metrics = {"requests": 0, "errors": 0}
    logger.info("Application dependencies initialized")
    yield
    logger.info("Shutting down RAG API application")
    background_service = getattr(app.state, "background_ingestion", None)
    if background_service is not None:
        background_service.shutdown()


def _ensure_metrics(app_state) -> dict[str, int]:
    metrics = getattr(app_state, "metrics", None)
    if metrics is None:
        metrics = {"requests": 0, "errors": 0}
        app_state.metrics = metrics
    return metrics


app = FastAPI(
    title="RAG System API",
    version="1.0.0",
    description="Production-grade RAG backend built without LangChain or LlamaIndex.",
    lifespan=lifespan,
)


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    path = request.url.path
    app_state = request.app.state
    metrics = _ensure_metrics(app_state)
    metrics["requests"] = int(metrics.get("requests", 0)) + 1

    if path not in PUBLIC_PATHS and not path.startswith("/static"):
        api_keys = get_api_keys()
        if api_keys:
            provided_api_key = request.headers.get("X-API-Key") or request.headers.get("Authorization", "").replace("Bearer ", "", 1).strip()
            if provided_api_key not in api_keys:
                metrics["errors"] = int(metrics.get("errors", 0)) + 1
                return JSONResponse(status_code=401, content={"detail": "Invalid or missing API key."})

        client_ip = request.client.host if request.client else "unknown"
        if not rate_limiter.allow(client_ip):
            metrics["errors"] = int(metrics.get("errors", 0)) + 1
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded. Try again later."})

    response = await call_next(request)
    if response.status_code >= 500:
        metrics["errors"] = int(metrics.get("errors", 0)) + 1
    return response


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins() or ["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(search_router)
app.include_router(ask_router)