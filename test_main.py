from fastapi.testclient import TestClient
from app.main import app
import json

client = TestClient(app)

def test_get_static_content():
    response = client.get("/api/static-content")
    assert response.status_code == 200
    data = response.json()
    assert "election_process" in data
    assert "faqs" in data

def test_eligibility_eligible():
    response = client.post(
        "/api/eligibility",
        json={"age": 18, "is_citizen": True}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "eligible"

def test_eligibility_ineligible_age():
    response = client.post(
        "/api/eligibility",
        json={"age": 17, "is_citizen": True}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ineligible"

def test_eligibility_ineligible_citizen():
    response = client.post(
        "/api/eligibility",
        json={"age": 25, "is_citizen": False}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "ineligible"

def test_chat_empty_message():
    response = client.post(
        "/api/chat",
        json={"message": "   "}
    )
    assert response.status_code == 422
