import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

import google.cloud.firestore
import google.cloud.texttospeech
import vertexai

# Mock Google Cloud libraries before importing the app
with patch('google.cloud.firestore.Client'), \
     patch('google.cloud.texttospeech.TextToSpeechClient'), \
     patch('vertexai.init'), \
     patch('vertexai.generative_models.GenerativeModel'):
    from app.main import app

@pytest.fixture
def client():
    """FastAPI test client fixture."""
    with TestClient(app) as c:
        yield c

@pytest.fixture(autouse=True)
def mock_services():
    """Automatically mock external services for all tests."""
    with patch('app.services.firestore_service.firestore_service.db') as mock_db, \
         patch('app.services.gemini_service.gemini_service.model') as mock_model, \
         patch('app.services.tts_service.tts_service.client') as mock_tts:
        
        # Setup Firestore mock
        mock_doc = MagicMock()
        mock_doc.to_dict.return_value = {"question": "Test FAQ?", "answer": "Test Answer"}
        mock_db.collection.return_value.stream.return_value = [mock_doc]
        
        # Setup Gemini mock
        mock_response = MagicMock()
        mock_response.text = "Mocked AI response"
        mock_model.generate_content.return_value = mock_response
        
        # Setup TTS mock
        mock_tts_response = MagicMock()
        mock_tts_response.audio_content = b"mock_audio_data"
        mock_tts.synthesize_speech.return_value = mock_tts_response
        
        yield {
            "db": mock_db,
            "model": mock_model,
            "tts": mock_tts
        }
