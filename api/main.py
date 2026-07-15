import logging
from contextlib import asynccontextmanager
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

from api.dependencies import create_app_dependencies
from api.routes.ask import router as ask_router
from api.routes.health import router as health_router
from api.routes.search import router as search_router
from api.routes.upload import router as upload_router
from configs.logging_config import logger
from services.background_ingestion import BackgroundIngestionService


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting RAG API application")
    app.state.dependencies = create_app_dependencies()
    app.state.background_ingestion = BackgroundIngestionService()
    logger.info("Application dependencies initialized")
    yield
    logger.info("Shutting down RAG API application")
    background_service = getattr(app.state, "background_ingestion", None)
    if background_service is not None:
        background_service.shutdown()


app = FastAPI(
    title="RAG System API",
    version="1.0.0",
    description="Production-grade RAG backend built without LangChain or LlamaIndex.",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(search_router)
app.include_router(ask_router)