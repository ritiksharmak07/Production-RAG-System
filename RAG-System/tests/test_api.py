import os

from fastapi.testclient import TestClient

os.environ["API_KEYS"] = "test-key"
os.environ["CORS_ALLOWED_ORIGINS"] = "http://localhost:3000,http://127.0.0.1:3000"

from api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_service_liveness_and_readiness_endpoints():
    assert client.get("/health/live").status_code == 200
    assert client.get("/health/ready").status_code == 200


def test_search_requires_api_key():
    response = client.get("/search/?query=python")
    assert response.status_code == 401

    response = client.get("/search/?query=python", headers={"X-API-Key": "test-key"})
    assert response.status_code == 404


def test_upload_rejects_unsupported_file_type():
    files = {"files": ("notes.exe", b"not-a-real-file", "application/x-msdownload")}
    response = client.post("/upload/files", files=files, headers={"X-API-Key": "test-key"})
    assert response.status_code == 400
