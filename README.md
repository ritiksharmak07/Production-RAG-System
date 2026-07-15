# RAG System

A production-oriented retrieval-augmented generation system built without LangChain or LlamaIndex, featuring a Python backend, document ingestion pipeline, retrieval, reranking, and a React frontend.

## Requirements

- Python 3.11+ (or compatible Python 3.10+)
- Node.js 20+ / npm 10+ for the frontend
- `venv` or another Python virtual environment manager

## Python dependencies

The backend requirements are declared in `requirements.txt`:

```txt
pypdf
python-docx
pandas
requests==2.32.0
google-generativeai
python-dotenv
```

## Frontend dependencies

The frontend package manifest is located at `RAG-System/frontend/package.json` and includes React, Vite, Tailwind, TanStack Query, React Router, Axios, Zustand, Framer Motion, and testing tools.

## Frontend scripts

Use the following commands inside `RAG-System/frontend`:

```bash
npm run dev
npm run build
npm run preview
npm test
```

## Developer dependencies

For backend development tooling, install:

```bash
pip install -r requirements-dev.txt
```

## Quick start

1. Create and activate a Python virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install backend dependencies:

```bash
pip install -r requirements.txt
```

3. Install frontend dependencies:

```bash
cd frontend
npm install
```

4. Run the backend API (from `RAG-System`):

```bash
uvicorn api.main:app --reload --port 8000
```

5. Run the frontend:

```bash
cd RAG-System/frontend
npm run dev
```

## Notes

- Uploads are validated and ingested through the backend upload endpoint.
- The frontend proxies `/api` to the backend when running locally.
- The project includes search, chat, and upload experiences.
