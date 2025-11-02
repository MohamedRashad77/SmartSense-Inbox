import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_summarize_sms():
    response = client.post("/api/v1/summarize", json={"sms": ["Hello, how are you?", "Don't forget the meeting at 10 AM."]})
    assert response.status_code == 200
    assert "summary" in response.json()
    assert response.json()["summary"] == "Meeting reminder and greeting."

def test_empty_sms_list():
    response = client.post("/api/v1/summarize", json={"sms": []})
    assert response.status_code == 400
    assert response.json()["detail"] == "SMS list cannot be empty."