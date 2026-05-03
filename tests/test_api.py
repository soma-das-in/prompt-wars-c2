import pytest
from app.services.gemini_service import gemini_service
from app.services.tts_service import tts_service

def test_root_serves_index(client):
    """Test that the root URL serves index.html."""
    response = client.get("/")
    assert response.status_code == 200
    assert "VoteAssist" in response.text

def test_get_static_content(client):
    """Test fetching FAQs from Firestore."""
    response = client.get("/api/static-content")
    assert response.status_code == 200
    data = response.json()
    assert "faqs" in data
    assert len(data["faqs"]) > 0
    assert data["faqs"][0]["question"] == "Test FAQ?"

def test_eligibility_eligible(client):
    """Test positive eligibility check."""
    response = client.post("/api/eligibility", json={"age": 18, "is_citizen": True})
    assert response.status_code == 200
    assert response.json()["status"] == "eligible"

def test_eligibility_ineligible_age(client):
    """Test ineligible age."""
    response = client.post("/api/eligibility", json={"age": 17, "is_citizen": True})
    assert response.status_code == 200
    assert response.json()["status"] == "ineligible"
    assert "18 years old" in response.json()["message"]

def test_eligibility_invalid_input(client):
    """Test invalid input validation."""
    # Negative age
    response = client.post("/api/eligibility", json={"age": -1, "is_citizen": True})
    assert response.status_code == 422
    
    # Missing field
    response = client.post("/api/eligibility", json={"age": 20})
    assert response.status_code == 422

def test_chat_success(client):
    """Test successful chat interaction."""
    response = client.post("/api/chat", json={"message": "How do I register?"})
    assert response.status_code == 200
    assert response.json()["reply"] == "Mocked AI response"

def test_chat_validation(client):
    """Test chat message validation."""
    # Empty message
    response = client.post("/api/chat", json={"message": ""})
    assert response.status_code == 422
    
    # Message too long
    response = client.post("/api/chat", json={"message": "a" * 501})
    assert response.status_code == 422

def test_tts_success(client):
    """Test successful TTS synthesis."""
    response = client.post("/api/tts", json={"text": "Hello"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "audio/mpeg"
    assert response.content == b"mock_audio_data"

def test_tts_validation(client):
    """Test TTS input validation."""
    response = client.post("/api/tts", json={"text": "a" * 201})
    assert response.status_code == 422

def test_chat_server_error(client, mock_services):
    """Test API response when Gemini fails."""
    gemini_service.generate_response.cache_clear()
    mock_services["model"].generate_content.side_effect = Exception("Model Error")
    response = client.post("/api/chat", json={"message": "Hello error"})
    # The service returns a generic safe message string, not a 500 error raised to FastAPI
    assert response.status_code == 200
    assert "error occurred" in response.json()["reply"]

def test_tts_server_error(client, mock_services):
    """Test API response when TTS fails."""
    tts_service._get_cached_synthesis.cache_clear()
    mock_services["tts"].synthesize_speech.side_effect = Exception("TTS Error")
    response = client.post("/api/tts", json={"text": "Hello failure"})
    assert response.status_code == 500
