import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_tts_endpoint():
    response = client.post("/tts", json={"text": "Hello world", "voice": "en-US-AriaNeural"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    # Note: In a real test, you might want to check the file content, but for now, just check response