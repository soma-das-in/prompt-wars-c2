from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field, validator
from app.services.firestore_service import firestore_service
from app.services.gemini_service import gemini_service
from app.services.tts_service import tts_service
from app.config import settings
from app.limiter import limiter

router = APIRouter(prefix="/api")

# Pydantic models for request validation
class EligibilityRequest(BaseModel):
    age: int = Field(..., ge=1, le=120)
    is_citizen: bool

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=settings.MAX_QUERY_LENGTH)

    @validator('message')
    def sanitize_message(cls, v):
        # Remove any potential malicious characters or excess whitespace
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be empty")
        return v

class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=200)

@router.get("/static-content")
@limiter.limit(settings.CONTENT_LIMIT)
async def get_static_content(request: Request):
    """Fetches FAQs from Firestore."""
    faqs = firestore_service.get_faqs()
    return {"faqs": faqs}

@router.post("/eligibility")
async def check_eligibility(req: EligibilityRequest):
    """Checks voter eligibility based on age and citizenship."""
    if req.age >= 18 and req.is_citizen:
        return {"status": "eligible", "message": "You are eligible to register as a voter."}
    
    reasons = []
    if req.age < 18:
        reasons.append("you must be at least 18 years old")
    if not req.is_citizen:
        reasons.append("you must be an Indian citizen")
    
    reason_str = " and ".join(reasons)
    return {"status": "ineligible", "message": f"You are not eligible because {reason_str}."}

@router.post("/chat")
@limiter.limit(settings.CHAT_LIMIT)
async def chat_with_assistant(request: Request, req: ChatRequest):
    """Main chat endpoint interacting with Gemini."""
    reply = gemini_service.generate_response(req.message)
    return {"reply": reply}

@router.post("/tts")
@limiter.limit(settings.TTS_LIMIT)
async def text_to_speech(request: Request, req: TTSRequest):
    """Converts response text to audio stream."""
    audio_stream = tts_service.synthesize(req.text)
    if not audio_stream:
        raise HTTPException(status_code=500, detail="Failed to synthesize speech")
    
    return StreamingResponse(audio_stream, media_type="audio/mpeg")
