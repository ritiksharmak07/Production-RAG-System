from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_search_without_index_returns_404():
    response = client.get("/search/?query=python")
    assert response.status_code == 404


def test_upload_rejects_unsupported_file_type():
    files = {"files": ("notes.exe", b"not-a-real-file", "application/x-msdownload")}
    response = client.post("/upload/files", files=files)
    assert response.status_code == 400
