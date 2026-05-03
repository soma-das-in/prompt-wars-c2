from google.cloud import texttospeech
import io
import logging
from functools import lru_cache

logger = logging.getLogger(__name__)

class TTSService:
    """
    Service to handle interactions with Google Cloud Text-to-Speech.
    Uses LRU caching to avoid redundant API calls for identical text.
    """
    
    def __init__(self):
        self.client = texttospeech.TextToSpeechClient()

    def synthesize(self, text: str) -> io.BytesIO:
        """Converts text to speech with caching."""
        # Safety: Ensure text is within reasonable bounds
        if len(text) > 150:
            text = text[:147] + "..."

        audio_content = self._get_cached_synthesis(text)
        if not audio_content:
            return None
            
        return io.BytesIO(audio_content)

    @lru_cache(maxsize=50)
    def _get_cached_synthesis(self, text: str) -> bytes:
        """Internal method to handle cached synthesis calls."""
        lang_code = self._detect_language(text)

        input_text = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        try:
            response = self.client.synthesize_speech(
                input=input_text, voice=voice, audio_config=audio_config
            )
            return response.audio_content
        except Exception:
            logger.error("TTS synthesis failed")
            return None

    def _detect_language(self, text: str) -> str:
        """Basic detection for Hindi, Bengali, or English."""
        if any("\u0900" <= c <= "\u097F" for c in text):
            return "hi-IN"
        elif any("\u0980" <= c <= "\u09FF" for c in text):
            return "bn-IN"
        return "en-IN"

# Singleton instance
tts_service = TTSService()
